from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


@dataclass
class Request:
    from_floor: int
    to_floor: int

    @property
    def direction(self) -> Direction:
        if self.to_floor > self.from_floor:
            return Direction.UP
        elif self.to_floor < self.from_floor:
            return Direction.DOWN
        return Direction.IDLE
