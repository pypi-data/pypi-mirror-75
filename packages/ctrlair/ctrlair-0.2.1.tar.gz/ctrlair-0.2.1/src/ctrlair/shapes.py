from typing import NamedTuple

Shape = NamedTuple("Shape", [("Name", str), ("Path", str)])

square = Shape("Square", "M -1 1 L 1 1 L 1 -1 L -1 -1 Z")
circle = Shape(
    "Circle", "M -1 0 A 1 1 0 0 0 0 1 A 1 1 0 0 0 1 0 A 1 1 0 0 0 0 -1 A 1 1 0 0 0 -1 0"
)
diamond = Shape("Diamond", "M 0 -1 L 1 0 L 0 1 L -1 0 Z")

up_pointing_triangle = Shape("Up-Pointing Triangle", "M 0 -1 L -1 1 L 1 1 Z")
down_pointing_triangle = Shape("Down-Pointing Triangle", "M 0 1 L -1 -1 L 1 -1 Z")
left_pointing_triangle = Shape("Left-Pointing Triangle", "M -1 0 L 1 1 L 1 -1 Z")
right_pointing_triangle = Shape("Right-Pointing Triangle", "M 1 0 L -1 1 L -1 -1 Z")

star = Shape(
    "Star",
    "M 0 0.6 L 0.6 0.9 L 0.5 0.2 L 1 -0.2 L 0.3 -0.3 L 0 -0.9 L -0.3 -0.3 L -1 -0.2 L -0.5 0.2 L -0.6 0.9 L 0 0.6 Z",
)

times = Shape("Times", "M 1 1 L -1 -1 M -1 1 L 1 -1")
plus = Shape("Plus", "M 0 1 L 0 -1 M -1 0 L 1 0")
minus = Shape("Minus", "M -1 0 L 1 0")

lower_right_triangle = Shape("Lower Right Triangle", "M -1 1 L 1 -1 L 1 1 Z")
lower_left_triangle = Shape("Lower Left Triangle", "M 1 1 L -1 -1 L -1 1 Z")
upper_right_triangle = Shape("Upper Right Triangle", "M 1 1 L -1 -1 L 1 -1 Z")
upper_left_triangle = Shape("Upper Left Triangle", "M -1 1 L -1 -1 L 1 -1 Z")

left_pointing_squared_petal = Shape(
    "Left-Pointing Squared Petal", "M -1 0 L 0 1 A 1 1 0 0 0 0 -1 L 0 -1 Z"
)
right_pointing_squared_petal = Shape(
    "Right-Pointing Squared Petal", "M 1 0 L 0 -1 A 1 1 0 0 0 0 1 L 1 0 Z"
)
up_pointing_squared_petal = Shape(
    "Up-Pointing Squared Petal", "M 0 -1 L -1 0 A 1 1 0 0 0 1 0 L 1 0 Z"
)
down_pointing_squared_petal = Shape(
    "Down-Pointing Squared Petal", "M 0 1 L 1 0 A 1 1 0 0 0 -1 0 L -1 0 Z"
)

shield = Shape("Shield", "M -1 -1 L -1 0 A 1 1 0 0 0 1 0 L 1 -1 Z")

up_pointing_angle_bracket = Shape(
    "Up-Pointing Angle Bracket", "M 0 -1 L 1 0 L 1 1 L 0 0 L -1 1 L -1 0 Z"
)

hourglass = Shape("Hourglass", "M -1 -1 L 1 -1 L -1 1 L -1 1 L 1 1 L -1 -1 Z")
horizontal_hourglass = Shape(
    "Horizontal Hourglass", "M 1 1 L 1 -1 L -1 1 L -1 1 L -1 -1 L 0 0 Z"
)

rounded_tip = Shape(
    "Rounded Tip", "M -1 1 C -1 1 -1 -0.3333 0 -1 C 1 -0.3333 1 1 1 1 Z"
)

south_east_arrow_tip = Shape(
    "South East Arrow Tip", "M 0 -1 L 1 1 L -1 0 L -1 0 L 0 0 Z"
)
north_west_arrow_tip = Shape(
    "North West Arrow Tip", "M 1 0 L -1 -1 L 0 1 L 0 1 L 0 0 Z"
)

south_east_squared_arrow_tip = Shape(
    "South East Squared Arrow Tip", "M -1 -1 L -1 -1 L 0 -1 L 1 1 L -1 0 Z"
)

lower_left_vertical_parallelogram = Shape(
    "Vertical Parallelogram (Lower Left to Upper Right)",
    "M 0 -1 L 1 -1 L 0 1 L -1 1 L 0 -1 Z",
)
upper_left_vertical_parallelogram = Shape(
    "Vertical Parallelogram (Upper Left to Lower Right)",
    "M 0 -1 L 1 1 L 0 1 L -1 -1 L 0 -1 Z",
)

heart = Shape("Heart", "M 1 0 L 0 1 L -1 0 A 0.4 0.4 0 0 1 0 -1 A 0.4 0.4 0 0 1 1 0")
