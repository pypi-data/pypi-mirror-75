import contextlib
import datetime
import sqlite3
import statistics
from typing import Callable, Optional, Sequence, Tuple
import uuid

from docbrown.models import calculate_progress, PassedPhase, Progress, Timings
from docbrown.storage import StorageBackend


TimingsResultSet = Sequence[Tuple[str, float]]
AggregatorFunc = Callable[[sqlite3.Cursor, str], TimingsResultSet]


def aggregate_avg(cursor: sqlite3.Cursor, aggregator_key: str) -> TimingsResultSet:
    cursor.execute('SELECT phase, AVG(duration) AS duration FROM timings '
                   'WHERE aggregator_key = ? GROUP BY phase ORDER BY ordinal', [aggregator_key])
    return cursor.fetchall()


def aggregate_median(cursor: sqlite3.Cursor, aggregator_key: str) -> TimingsResultSet:
    class Median:
        def __init__(self):
            self.values = []

        def step(self, value):
            self.values.append(value)

        def finalize(self):
            return statistics.median(self.values)
    cursor.connection.create_aggregate('MEDIAN', 1, Median)
    cursor.execute('SELECT phase, MEDIAN(duration) AS duration FROM timings '
                   'WHERE aggregator_key = ? GROUP BY phase ORDER BY ordinal', [aggregator_key])
    return cursor.fetchall()


class SQLiteBackend(StorageBackend):
    MIGRATIONS = (
        (
            "CREATE TABLE metadata (meta_key TEXT NOT NULL UNIQUE, "
            "                       meta_value TEXT NOT NULL);",
            "CREATE TABLE timings (aggregator_key TEXT NOT NULL, "
            "                      phase TEXT NOT NULL, "
            "                      duration REAL NOT NULL);",
            "CREATE TABLE progress (ident TEXT NOT NULL, "
            "                       aggregator_key TEXT NOT NULL, "
            "                       phase TEXT NOT NULL, "
            "                       entered_at TEXT NOT NULL);",
        ),
        (
            "ALTER TABLE timings ADD COLUMN ordinal INTEGER",
        ),
        (
            "ALTER TABLE progress ADD COLUMN process_uuid TEXT",
        )
    )

    def __init__(self, db_file):
        self.db_file = db_file
        self._run_migrations()

    @contextlib.contextmanager
    def _cursor(self):
        connection = sqlite3.connect(self.db_file)
        try:
            yield connection.cursor()
        finally:
            connection.commit()
            connection.close()

    def _run_migrations(self):
        migration_version = None
        with self._cursor() as cursor:
            try:
                cursor.execute('SELECT meta_value FROM metadata WHERE meta_key = "version";')
                version = int(cursor.fetchone()[0])
            except sqlite3.OperationalError:
                version = 0
            for offset, migration in enumerate(self.MIGRATIONS[version:]):
                migration_version = version + offset + 1
                for step in migration:
                    cursor.execute(step)
            if migration_version is not None:
                cursor.execute('REPLACE INTO metadata(meta_key, meta_value) VALUES (?, ?);',
                               ('version', migration_version))

    def store_timings(self, ident, aggregator_key: str, timings: Timings) -> None:
        with self._cursor() as cursor:
            for index, (phase, duration) in enumerate(timings.items()):
                cursor.execute(
                    'INSERT INTO timings(aggregator_key, phase, duration, ordinal) '
                    'VALUES (?, ?, ?, ?);',
                    (aggregator_key, phase, duration, index))
        self.clear_progress(ident)

    def store_progress(self, ident: str, process_uuid: uuid.UUID, aggregator_key: str, phase: str,
                       entered_at: datetime.datetime) -> None:
        with self._cursor() as cursor:
            cursor.execute(
                'INSERT INTO progress(ident, process_uuid, aggregator_key, phase, entered_at) '
                'VALUES(?, ?, ?, ?, ?);',
                [ident, str(process_uuid), aggregator_key, phase, entered_at.isoformat()])

    def clear_progress(self, ident: str) -> None:
        with self._cursor() as cursor:
            cursor.execute('DELETE FROM progress WHERE ident = ?', [ident])

    def get_progress(self, ident: str, aggregator_func: AggregatorFunc) -> Optional[Progress]:
        now = datetime.datetime.now()
        aggregator_func = aggregate_avg if aggregator_func is None else aggregator_func

        with self._cursor() as cursor:
            cursor.execute('SELECT aggregator_key, process_uuid, phase, entered_at '
                           'FROM progress '
                           'WHERE ident = ? '
                           'ORDER BY entered_at;', [ident])
            passed_phases = cursor.fetchall()
            if len(passed_phases) == 0:
                return None

        aggregator_key = passed_phases[-1][0]
        process_uuid = passed_phases[-1][1]
        with self._cursor() as cursor:
            timings = aggregator_func(cursor, aggregator_key)
            if len(timings) == 0:
                return None

        timings = {phase: duration for phase, duration in timings}
        passed_phases = [PassedPhase(phase, datetime.datetime.fromisoformat(entered_at))
                         for _, _, phase, entered_at in passed_phases]
        progress = calculate_progress(passed_phases, timings, now)
        progress.process_uuid = uuid.UUID(process_uuid)
        return progress
