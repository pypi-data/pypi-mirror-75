"""This package contains various functions pertaining to 2d movement."""

from math import cos, pi, sin
from typing import List, Tuple

__all__: List[str] = [
    'normalise_angle', 'angle2rad', 'coordinates_in_direction'
]


def normalise_angle(angle: int) -> int:
    """Return an angle between 0 and 359 degrees. If it is more or less
    than that, it will wrap around."""
    if angle < 0:
        return angle + 360
    elif angle > 359:
        return angle - 360
    return angle


def angle2rad(angle: int) -> float:
    """Converts an angle to radians. Formula taken from
    https://synthizer.github.io/tutorials/python.html"""
    return (angle / 180.0) * pi


def coordinates_in_direction(
    start_x: float, start_y: float, angle: int, distance: float = 1.0
) -> Tuple[float, float]:
    """Returns the coordinates that lie distance in direction from (start_x,
    start_y)."""
    rad: float = angle2rad(angle)
    x: float = start_x + (distance * sin(rad))
    y: float = start_y + (distance * cos(rad))
    return x, y
