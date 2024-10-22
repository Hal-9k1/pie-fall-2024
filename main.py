from controller import RobotController
from layer.controls import BumperControls
from layer.controls import GamepadInputGenerator
from layer.controls import TankDriveControls
from layer.controls import ZeldaControls
from layer.drive import TwoWheelDrive
from layer.strategy import CubeDropStrategy
from layer.strategy import CubePlateStrategy
from layer.strategy import SafeStrategy
from layer.strategy import SimpleDriveTest
from mock_robot import MockRobot
from sys import stdout
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_out = logging.StreamHandler(stdout)
log_out.setFormatter(logging.Formatter("[%(levelname)s %(name)s] %(message)s"))
logger.addHandler(log_out)

def is_dawn():
    try:
        Robot
        return True
    except NameError:
        return False

def get_robot():
    if is_dawn():
        return Robot
    else:
        return MockRobot({
            "koalabear": 2,
            "servocontroller": 0,
        })

auto_layer_classes = [
    TwoWheelDrive,
    SimpleDriveTest
]
teleop_layer_classes = [
    TwoWheelDrive,
    ZeldaControls,
    GamepadInputGenerator,
]
robot_controller = RobotController()

@_PREP_ENTRY_POINT
def autonomous_setup():
    robot_controller.setup(get_robot(), auto_layer_classes)
@_PREP_ENTRY_POINT
def autonomous_main():
    if robot_controller.update() and not is_dawn():
        exit(0)
@_PREP_ENTRY_POINT
def teleop_setup():
    robot_controller.setup(get_robot(), teleop_layer_classes)
@_PREP_ENTRY_POINT
def teleop_main():
    if robot_controller.update() and not is_dawn():
        exit(0)
