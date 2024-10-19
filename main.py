#from layer.drive import TwoWheelDrive
#from layer import SimpleDriveTest
#from layer.controls import TankDriveControls
#from layer.controls import GamepadInputGenerator
from controller import RobotController
from mock_robot import MockRobot

try:
    robot = Robot
    is_dawn = True
except NameError:
    robot = MockRobot({
        "koalabear": 0,
        "servocontroller": 0,
    })
    is_dawn = False
auto_layer_classes = [
#    TwoWheelDrive,
#    SimpleDriveTest,
    RestaurantPrinter,
    RestaurantSectionLayer,
    RestaurantMenuSource,
]
teleop_layer_classes = [
#    TwoWheelDrive,
#    TankDriveControls,
#    GamepadInputGenerator,
]
robot_controller = RobotController(robot)

@_PREP_ENTRY_POINT
def autonomous_setup():
    robot_controller.setup(auto_layer_classes)
@_PREP_ENTRY_POINT
def autonomous_main():
    if robot_controller.update() and not is_dawn:
        exit(0)
@_PREP_ENTRY_POINT
def teleop_setup():
    robot_controller.setup(teleop_layer_classes)
@_PREP_ENTRY_POINT
def teleop_main():
    if robot_controller.update() and not is_dawn:
        exit(0)
