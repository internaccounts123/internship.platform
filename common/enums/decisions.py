from enum import Enum


class Decisions(Enum):
    Accelerate = 1
    De_accelerate = 2
    Constant_speed = 3
    Lane_change = 4
    Move_right = 5
    Move_left = 6
    Positive = 7
