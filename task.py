from dataclasses import dataclass


class UnsupportedTaskError(TypeError):
    """Exception raised by layers when accepting a task type they don't support."""

    def __init__(self, layer, task):
        super().__init__(f"Layer '{type(layer).__name__}' does not support task of type"
            f" '{type(task).__name__}'.")


@dataclass
class AxialMovementTask:
    """Moves the robot forwards or backwards by a distance."""

    """The distance in meters to move the robot forward.

    Negative values indicate backward movement.
    """
    distance: float


@dataclass
class TurnTask:
    """Turn the robot in place."""

    """The angle in radians to turn the robot counterclockwise.

    Negative values indicate clockwise turns.
    """
    angle: float


@dataclass
class TankDriveTask:
    """Specifies relative accelerations for left and right side of the robot.

    Despite the name, not necessarily produced by tank drive controls."""

    """The relative acceleration to apply to the left side of the robot.

    Positive values indicate forward movement and negative values indicate backward."""
    left: float

    """The relative acceleration to apply to the right side of the robot.

    Positive values indicate forward movement and negative values indicate backward."""
    right: float
