from layer import Layer
from layer import InputGenerator
from task import GamepadInputTask
from task import TankDriveTask
from task import UnsupportedTaskError


class GamepadInputGenerator(InputGenerator):
    """Generates Gamepad input tasks"""

    def __init__(self, init_info):
        pass

    def update(self):
        return GamepadInputTask(
            joystick_left_x=Gamepad.get_value("joystick_left_x"),
            joystick_left_y=Gamepad.get_value("joystick_left_y"),
            joystick_right_x=Gamepad.get_value("joystick_right_x"),
            joystick_right_y=Gamepad.get_value("joystick_right_y"),
            button_a=Gamepad.get_value("button_a"),
            button_b=Gamepad.get_value("button_b"),
            button_x=Gamepad.get_value("button_x"),
            button_y=Gamepad.get_value("button_y"),
            left_bumper=Gamepad.get_value("l_bumper"),
            left_trigger=Gamepad.get_value("l_trigger"),
            right_bumper=Gamepad.get_value("r_bumper"),
            right_trigger=Gamepad.get_value("r_trigger"),
        )


class TankDriveControls(Layer):
    """Tank drive mappings for gamepad and keyboard inputs.

    Left and right stick y control left and right motors.
    """

    def __init__(self, init_info):
        pass

    def is_task_done(self):
        return True

    def update(self):
        return self._subtask

    def accept_task(self, task):
        if isinstance(task, GamepadInputTask):
            left = task.joystick_left_y
            right = task.joystick_right_y
        else:
            raise UnsupportedTaskError(self, task)
        self._subtask = TankDriveTask(left, right)


class ZeldaControls(Layer):
    """'Zelda' style mappings for gamepad and keyboard inputs.

    Left stick y is axial movement, left stick x is turning.
    """

    def __init__(self, init_info):
        pass

    def is_task_done(self):
        return True

    def update(self):
        return self._subtask

    def accept_task(self, task):
        if isinstance(task, GamepadInputTask):
            axial = task.joystick_left_y
            turn = task.joystick_left_x
        else:
            raise UnsupportedTaskError(self, task)
        self._subtask = TankDriveTask(axial - turn, axial + turn)


class BumperControls(Layer):
    """Mappings that use the bumpers to turn and joystick to drive.

    Inspired by Live Oak's mapping. Accepts gamepad inputs only. Left stick y
    drives, bumpers turn.
    """

    def __init__(self, init_info):
        pass

    def is_task_done(self):
        return True

    def update(self):
        return self._subtask

    def accept_task(self, task):
        if isinstance(task, GamepadInputTask):
            axial = task.joystick_left_y
            turn = 0
            if task.left_bumper:
                turn += 1
            if task.right_bumper:
                turn -= 1
        else:
            raise UnsupportedTaskError(self, task)
        self._subtask = TankDriveTask(axial - turn, axial + turn)
