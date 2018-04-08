from enum import IntEnum


class JobState(IntEnum):
    COMPLETED = 0
    RUNNING = 1
    FAILED = -1
