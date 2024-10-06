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
        """Performs incremental work and returns whether layers have completed all tasks.

        Performs incremental work on the bottommost layer, invoking upper layers as necessary when
        lower layers complete their current tasks. Returns whether the topmost layer (and by
        extension, every layer) are exhausted of tasks. When this happens, update listeners are
        notified and then unregistered.
        """
        # Call all update listeners
        for listener in self._update_listeners:
            listener(False)

        # Do work on layers
        i = 0 # Fallback in case of 0 layers which shouldn't happen anyways
        task = self # Use self as sentinel
        for i, layer in enumerate(self._layers):
            if not layer.is_task_done():
                task = layer.update()
                break
        if task is self:
            # No tasks left in any layer
            for listener in self._update_listeners:
                listener(True)
            self._update_listeners = []
            return True
        # Start at layer below first incomplete one and continue backwards to lowest layer
        for j in range(i - 1, -1, -1):
            self._layers[j].accept_task(task)
            task = self._layers[j].update()
        return False

    def add_update_listener(self, listener):
        """Registers a function to be called on every update().

        Registers a function to be called on every update of the controller before layer work is
        performed. Listeners are executed in registration order and called with a single positional
        argument of True. On the first update after the topmost layer runs out of tasks, the
        listeners are called again with an argument of False, then unregistered.

        Positional arguments:
        listener -- the function to be registered as an update listener
        """
        self._update_listeners.append(listener)
