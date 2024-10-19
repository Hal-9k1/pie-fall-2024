from layer import Layer
from layer import QueuedLayer
from units import convert
from task import UnsupportedTaskError
from task import AxialMovementTask

class CubeDropStrategy(QueuedLayer):
    """Ambitious autonomous strategy for maximum points.

    An ambitious autonomous strategy that leaves the starting room, pushes the cube off the ramp and
    ends on the left pressure plate. If starting in the right position, the robot will pass over the
    right pressure plate before continuing to the ramp.
    """

    def __init__(self, init_info):
        super().__init__(self, init_info)
        self._submit_subtask_queue([
            # Forward to left pressure plate:
            AxialMovementTask(convert(34, "in", "m")),
        ] if init_info.get_robot().start_pos == "left" else [
            # Forward to right pressure plate:
            AxialMovementTask(convert(34, "in", "m")),
            # Move to left pressure plate and face forward:
            TurnTask(convert(0.25, "rev", "rad")),
            AxialMovementTask(convert(18 + 6, "in", "m")),
            TurnTask(convert(-0.25, "rev", "rad")),
        ] + [
            # Forward up ramp, pushing cube over:
            AxialMovementTask(convert(12 + 30, "in", "m")),
            # Reverse down ramp and end on left plate:
            AxialMovementTask(convert(-12 - 30, "in", "m")),
        ])

    def accept_task(self, task):
        raise UnsupportedTaskError(self, task)


class CubePlateStrategy(QueuedLayer):
    """Ambitious autonomous strategy that insures against teammate malfunction.

    An ambitious autonomous strategy that leaves the starting room, retrieves the cube, and
    engages both pressure plates. Useful if the alliance partner's robot is unreliable or
    malfunctioning before the match.
    """

    def __init__(self, init_info):
        super().__init__(self, init_info)
        self._submit_subtask_queue([
            # Forward to left pressure plate:
            AxialMovementTask(convert(34, "in", "m")),
        ] if init_info.get_robot().start_pos == "left" else [
            # Forward to right pressure plate:
            AxialMovementTask(convert(34, "in", "m")),
            # Move to left pressure plate and face forward:
            TurnTask(convert(0.25, "rev", "rad")),
            AxialMovementTask(convert(18 + 6, "in", "m")),
            TurnTask(convert(-0.25, "rev", "rad")),
        ] + [
            # Forward up ramp:
            AxialMovementTask(convert(12 + 13, "in", "m")),
            # Grab cube,
            # Reverse down ramp:
            AxialMovementTask(convert(-12 - 13, "in", "m")),
            # Turn to right pressure plate and deposit cube:
            TurnTask(convert(-0.25, "rev", "rad")),
            AxialMovementTask(convert(16, "in", "m")),
            # Drop cube,
            # Reverse to end on left plate:
            AxialMovementTask(convert(-16, "in", "m")),
        ])

    def accept_task(self, task):
        raise UnsupportedTaskError(self, task)


class SafeStrategy(Layer):
    """Safest autonomous strategy.

    Just moves forward to sit on the pressure plate.
    """

    def __init__(self, init_info):
        self._task_emitted = False

    def is_task_done(self):
        return self._task_emitted

    def update(self):
        self._task_emitted = True
        return AxialMovementTask(convert(34, "in", "m"))

    def accept_task(self, task):
        raise UnsupportedTaskError(self, task)


class SimpleDriveTest(Layer):
    """Drives in a square indefinitely."""

    def __init__(self, init_info):
        self._straight = False # Inverted before first update

    def is_task_done(self):
        return False

    def update(self):
        self._straight = not self._straight
        if self._straight:
            return AxialMovementTask(convert(1, "m", "m"))
        else:
            return TurnTask(convert(-0.25, "rev", "rad"))

    def accept_task(self, task):
        raise UnsupportedTaskError(self, task)
