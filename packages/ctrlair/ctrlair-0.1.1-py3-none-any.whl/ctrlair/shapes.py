from collections import namedtuple

__all__ = ["square", "up_pointing_triangle", "star", "line_cross", "right_triangle"]

Shape = namedtuple("Shape", ["Name", "Path"])

square = Shape("Square", "M -1 1 L 1 1 L 1 -1 L -1 -1 Z")

up_pointing_triangle = Shape("Up-Pointing Triangle", "M 0 -1 L -1 1 L 1 1 Z")

star = Shape(
    "Star",
    "M 0 0.6 L 0.6 0.9 L 0.5 0.2 L 1 -0.2 L 0.3 -0.3 L 0 -0.9 L -0.3 -0.3 L -1 -0.2 L -0.5 0.2 L -0.6 0.9 L 0 0.6 Z",
)

line_cross = Shape("Line Cross", "M 1 1 L -1 -1 M -1 1 L 1 -1")

right_triangle = Shape("Right Triangle", "M 1 1 L -1 -1 L -1 1 Z")
