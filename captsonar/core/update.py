from enum import Enum

import numpy as np


class Direction(Enum):
    North = "North"
    South = "South"
    East = "East"
    West = "West"

    def to_offset(self):
        match self:
            case self.North:
                return (0, 1)
            case self.South:
                return (0, -1)
            case self.West:
                return (-1, 0)
            case self.East:
                return (1, 0)

    def __str__(self):
        return self.value


class DroneUpdate(object):
    def __init__(self, sector, positive):
        self.sector = sector
        self.positive = positive

    def __str__(self):
        return f"DroneUpdate({self.sector}, {self.positive})"


class SonarUpdate(object):
    def __init__(self, x: None | int, y: None | int, sector: None | int):
        self.x = x
        self.y = y
        self.sector = sector

    def __str__(self):
        return f"SonarUpdate({self.x}, {self.y}, {self.sector})"


class BombUpdate(object):
    def __init__(self, pos, damage):
        assert damage <= 2

        self.pos = pos
        self.damage = damage

    def __str__(self):
        return f"Bomb({self.pos}, {self.damage})"


class SilenceUpdate(object):
    def __str__(self):
        return "Silence"


class SurfaceUpdate(object):
    def __str__(self):
        return "Surface"


Move = (
    Direction | SilenceUpdate | SurfaceUpdate | BombUpdate | SonarUpdate | DroneUpdate
)
