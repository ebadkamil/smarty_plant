from enum import Enum


class OrderType(Enum):
    TYPE_A = "type_a"
    TYPE_B = "type_b"
    TYPE_C = "type_c"


class PipelineStatus(Enum):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"


class PipelineMode(Enum):
    STARTING = "Starting"
    STOPPING = "Stopping"
    RUNNING_NORMAL = "Running Normal"
    STANDING_STILL = "Standing Still"
