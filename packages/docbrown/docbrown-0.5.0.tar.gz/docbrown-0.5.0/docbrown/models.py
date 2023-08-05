import collections
import dataclasses
import datetime
from typing import List, Mapping, Sequence
from uuid import UUID


Timings = Mapping[str, float]
PassedPhase = collections.namedtuple('PassedPhase', ['phase', 'entered_at'])


@dataclasses.dataclass
class Progress:
    expected_duration: float
    passed_phases: List[str]
    expected_phases: List[str]
    current_phase: str
    phase_progress: float
    duration: float
    progress: float
    is_stuck: bool
    process_uuid: UUID = None

    def serialize(self):
        data = dataclasses.asdict(self)
        if self.process_uuid:
            data['process_uuid'] = str(self.process_uuid)
        return data


def _clamp_progress(progress):
    return min(100, max(0, progress * 100))


def calculate_progress(
        passed_phases: Sequence[PassedPhase],
        timings: Timings,
        now: datetime.datetime) -> Progress:
    current_phase = passed_phases[-1]
    current_phase_duration = (now - current_phase.entered_at).total_seconds()
    current_duration = (now - passed_phases[0].entered_at).total_seconds()
    empirical_total_duration = sum(timings.values())
    passed_phase_names = [phase.phase for phase in passed_phases]
    # We may encounter new phases that have not been recorded yet.
    # In these cases we just assume that the phase basically takes no time.
    empirical_phase_duration = timings.get(current_phase.phase, 0)

    # we calculate the expected duration as the total of
    #  * the time it took for previous phases to complete
    #  * the time that passed since the current phase was triggered
    #  * the time of each phase that was not triggered yet, based on empirical data.
    expected_total_duration = 0
    for index, phase in enumerate(passed_phases):
        try:
            next_phase = passed_phases[index + 1]
        except IndexError:
            break
        expected_total_duration += (next_phase.entered_at - phase.entered_at).total_seconds()
    expected_total_duration += max(current_phase_duration, empirical_phase_duration)
    for phase_name in timings.keys():
        if phase_name not in passed_phase_names:
            expected_total_duration += timings[phase_name]

    # calculate the progress as the total of
    #  * the time it took to complete passed phases as ratio
    #    in relation to the empirical total duration
    #  * the time spent in the current phase or the empirical time spent in the current phase
    #    as ratio in relation to the empirical total duration (whichever is smaller)
    total_progress = 0
    for phase in passed_phase_names:
        if phase != current_phase.phase:
            total_progress += (timings.get(phase, 0) / empirical_total_duration)
    empirical_phase_ratio = empirical_phase_duration / empirical_total_duration
    current_phase_ratio = current_phase_duration / empirical_total_duration
    # Use the minimum of both values because more time spent in this phase
    # does not mean that following phases will take less time. This will
    # cause the progress to get stuck in place, but avoids progress that
    # goes backwards or stays at 100% for prolonged periods of time.
    phase_progress_ratio = min(empirical_phase_ratio, current_phase_ratio)
    try:
        phase_progress = current_phase_duration / empirical_phase_duration
        # define a phase as stuck if it took 1.5 × the amount of time it usually does
        is_phase_stuck = current_phase_ratio / empirical_phase_ratio >= 1.5
    except ZeroDivisionError:
        phase_progress = 0
        is_phase_stuck = False
    total_progress += phase_progress_ratio

    expected_phases = list(timings.keys())
    expected_phases.remove('__startup__')

    return Progress(
        expected_duration=expected_total_duration,
        passed_phases=[phase.phase for phase in passed_phases],
        expected_phases=expected_phases,
        current_phase=current_phase.phase,
        phase_progress=_clamp_progress(phase_progress),
        duration=current_duration,
        progress=_clamp_progress(total_progress),
        is_stuck=is_phase_stuck,
    )
