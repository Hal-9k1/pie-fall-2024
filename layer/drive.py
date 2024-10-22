from actuators import Motor
from layer import Layer
from math import copysign
from mechanisms import Wheel
from task import AxialMovementTask
from task import TankDriveTask
from task import TurnTask
from task import UnsupportedTaskError
from units import convert


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

    """Unitless, experimentally determined constant (ew) measuring lack of friction. 

    Measures lack of friction between wheels and floor material. Goal delta distances are directly
    proportional to this.
    """
    _slipping_constant = 1

    def __init__(self, init_info):
        # Make sure to set ALL desired properties, even if they're defaults. The motor controller
        # might have remembered state from a different drive layer if it hasn't been power cycled
        # since then
        self._left_wheel = Wheel(
            Motor(init_info.get_robot(), self._drive_koalabear, "a")
                .set_invert(False)
                .set_pid(None, None, None),
            self._wheel_radius,
            self._ticks_per_rot)
        self._right_wheel = Wheel(
            Motor(init_info.get_robot(), self._drive_koalabear, "b")
                .set_invert(False)
                .set_pid(None, None, None),
            self._wheel_radius,
            self._ticks_per_rot)
        # Initial values not important, but they need to be defined for the first call to
        # is_task_done to not error
        self._left_start_pos = 0
        self._right_start_pos = 0
        # Task will appear done on first call to is_task_done
        self._left_goal_delta = 0
        self._right_goal_delta = 0

    def is_task_done(self):
        left_done = ((self._left_wheel.get_distance() - self._left_start_pos < 0)
            == (self._left_goal_delta < 0)) or self._left_goal_delta == 0
        right_done = ((self._right_wheel.get_distance() - self._right_start_pos < 0)
            == (self._right_goal_delta < 0)) or self._right_goal_delta == 0
        # A more intelligent system would detect whether both wheels are near their goals rather
        # than whether they have both passed them, but I'm not sure what to set the threshold at
        # without testing.
        done = left_done and right_done
        if done:
            # Setting motor velocities in a method meant to check state gives me the creeps, but
            # there's nowhere else to do it
            self._left_wheel.set_velocity(0)
            self._right_wheel.set_velocity(0)
        return done

    def update(self):
        pass # Adaptive velocity control should go here

    def accept_task(self, task):
        # Save current positions
        self._left_start_pos = self._left_wheel.get_distance()
        self._right_start_pos = self._right_wheel.get_distance()
        if isinstance(task, AxialMovementTask):
            self._left_goal_delta = task.distance
            self._right_goal_delta = task.distance
        elif isinstance(task, TurnTask):
            # "Effective" as in "multiplied by all the weird constants we need"
            effective_radius = self._wheel_span_radius * self._gear_ratio * self._slipping_constant
            self._left_goal_delta = -task.angle * effective_radius
            self._right_goal_delta = task.angle * effective_radius
        elif isinstance(task, TankDriveTask):
            # Teleop, set deltas to 0 to pretend we're done
            self._left_goal_delta = 0
            self._right_goal_delta = 0
            # Clamp to 1 to prevent upscaling
            max_abs_power = max(abs(task.left), abs(task.right), 1)
            self._left_wheel.set_velocity(task.left / max_abs_power)
            self._right_wheel.set_velocity(task.right / max_abs_power)
        else:
            raise UnsupportedTaskError(self, task)
        self._left_wheel.set_velocity(copysign(1, self._left_goal_delta))
        self._right_wheel.set_velocity(copysign(1, self._right_goal_delta))
