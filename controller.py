from layer import LayerSetupInfo

class RobotController:
    """Manages robot state between setup and the main loops."""

    def __init__(self, robot):
        """Creates a RobotController.

        Positional arguments:
        robot -- the Robot or Robot-like object used to communicate with hardware
        """
        self._layer_setup_info = LayerSetupInfo(robot, self)
        self._update_listeners = []

    def setup(self, layer_classes):
        """Initializes the controller with instances of the given layer classes.

        Positional arguments:
        layer_classes -- the list of layer classes, bottommost layer first
        """
        self._layers = [Class(self._layer_setup_info) for Class in layer_classes]

    def update(self):
        """Performs incremental work.

        Performs incremental work on the bottommost layer, invoking upper layers as necessary when
        lower layers complete their current tasks.
        """
        # Call all update listeners
        for listener in self._update_listeners:
            listener()

        # Do work on layers
        i = 0 # Fallback in case of 0 layers which shouldn't happen anyways
        task = self # Use self as sentinel
        for i, layer in enumerate(self._layers):
            if not layer.is_task_done():
                task = layer.update()
                break
        if task is self:
            # No tasks left in any layer
            return
        # Start at layer below first incomplete one and continue backwards to lowest layer
        for j in range(i - 1, -1, -1):
            self._layers[j].accept_task(task)
            task = self._layers[j].update()
