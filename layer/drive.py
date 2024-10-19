from actuators import Motor
from layer import Layer
from math import copysign
from mechanisms import Wheel
from task import AxialMovementTask
from task import TankDriveTask
from task import TurnTask
from task import UnsupportedTaskError
from unit import convert


class TwoWheelDrive(Layer):
    """Drive layer for a two-wheel drive robot."""

    """The id of the drive motor controller."""
    _drive_koalabear = "6_spamandeggs"
    """The number of encoder ticks per rotation of the drive motor shafts."""
    _ticks_per_rot = 888
    """The radius of the wheels in meters."""
    _wheel_radius = 0.42
    """The effective gear ratio of the wheels to the drive motor shafts.

    Expressed as wheel_teeth / hub_gear_teeth.
    """
    _gear_ratio = 1
    """Half the distance between the two driving wheels in meters."""
    _wheel_span_radius = 0.84

    def __init__(self, init_info):
        self._left_wheel = Wheel(
            Motor(init_info.get_robot(), self._drive_koalabear, "a/b")
                .set_invert(False)
                .set_pid(None, None, None),
            self._wheel_radius,
            self._ticks_per_rot)
        self._right_wheel = Wheel(
            Motor(init_info.get_robot(), self._drive_koalabear, "a/b")
                .set_invert(False)
                .set_pid(None, None, None),
            self._wheel_radius,
            self._ticks_per_rot)
        self._left_start_pos = 0
        self._right_start_pos = 0
        self._left_goal_delta = 0
        self._right_goal_delta = 0

    def is_task_done(self):
        left_done = ((self._left_wheel.get_distance() - self._left_start_pos < 0)
            == (self._left_goal_delta < 0)) or self._left_goal_delta == 0
        right_done = ((self._right_wheel.get_distance() - self._right_start_pos < 0)
            == (self._right_goal_delta < 0)) or self._right_goal_delta == 0
        done = left_done and right_done
        if done:
            self._left_wheel.set_velocity(0)
            self._right_wheel.set_velocity(0)
        return done

    def update(self):
        pass # Adaptive velocity control goes here

    def accept_task(self, task):
        self._left_start_pos = self._left_wheel.get_distance()
        self._right_start_pos = self._right_wheel.get_distance()
        if isinstance(task, AxialMovementTask):
            self._left_goal_delta = task.distance
            self._right_goal_delta = task.distance
        elif isinstance(task, TurnMovementTask):
            self._left_goal_delta = -task.angle * self._wheel_span_radius * self._gear_ratio
            self._right_goal_delta = task.angle * self._wheel_span_radius * self._gear_ratio
        elif isinstance(task, TankDriveTask):
            self._left_goal_delta = 0
            self._right_goal_delta = 0
            # Clamp to 1 to prevent upscaling:
            max_abs_power = max(abs(task.left), abs(task.right), 1)
            self._left_wheel.set_velocity(task.left / max_abs_power)
            self._right_wheel.set_velocity(task.right / max_abs_power)
        else:
            raise UnsupportedTaskError(self, task)
        self._left_wheel.set_velocity(copysign(1, self._left_goal_delta))
        self._right_wheel.set_velocity(copysign(1, self._right_goal_delta))
