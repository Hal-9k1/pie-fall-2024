from layer.drive import TwoWheelDrive
from layer import SimpleDriveTest
from layer.controls import TankDriveControls
from layer.controls import GamepadInputGenerator
from controller import RobotController

robot = Robot
auto_layer_classes = [
    TwoWheelDrive,
    SimpleDriveTest,
]
teleop_layer_classes = [
    TwoWheelDrive,
    TankDriveControls,
    GamepadInputGenerator,
]
robot_controller = RobotController(robot)

def autonomous_setup():
    robot_controller.setup(auto_layer_classes)
def autonomous_main():
    robot_controller.update()
def teleop_setup():
    robot_controller.setup(teleop_layer_classes)
def teleop_main():
    robot_controller.update()
