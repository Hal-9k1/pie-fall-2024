from abc import ABCMeta, abstractmethod
from task import UnsupportedTaskError


class Layer(metaclass=ABCMeta):
    """The base class of all layers.

    A layer is a modular unit of robot functionality. They interact with other layers by accepting
    tasks from the above layer and submitting tasks to the below layer. This represents the breaking
    down of a complex or abstract task into more simple and concrete ones.
    (A task is an instruction passed from a layer to its subordinate. Tasks range widely in their
    concreteness and can be as vague as "win the game" or as specific as "move forward 2 meters.")
    """

    @abstractmethod
    def is_task_done(self):
        """Returns whether the layer is ready to accept a new task.

        Returns True if the layer has finished processing the last accepted task, if any.
        """
        raise NotImplemented

    @abstractmethod
    def update(self):
        """Returns the next subordinate task produced from this layer's current task.

        Calculates the next subordinate task that should be submitted to the below layer. The return
        value of a bottom layer's update function is not used.
        """
        raise NotImplemented

    @abstractmethod
    def accept_task(self, task):
        """Sets the layer's current task.

        Accepts a task from the above layer. Should only be called after is_task_done() returns
        True.
        """
        raise NotImplemented


class InputGenerator(Layer):
    """The base class of input generating teleop layers.

    Input generators will be asked for a new task every robot update. This task should be to process
    the just-captured user input stored. Input generating layers must never present as done, which
    would prevent the layer and everything below it from ever again being updated by the controller
    in the likely case that the input generator is the top layer.
    """

    def is_task_done(self):
        return False

    def accept_task(self, task):
        raise UnsupportedTaskError(self, task)


class QueuedLayer(Layer):
    """The base class of layers that produce a queue of subtasks for each accepted task.

    Layers should inherit from this class if each call to accept_task generates a queue of subtasks
    to return from update, and no additional processing is needed in the update function.
    """

    """Sentinel value indicating that there is no next subtask, since None is a valid value."""
    _no_subtask = object()

    """Sentinel value indicating the next subtask should be retrieved from the queue."""
    _consumed_subtask = object()

    def __init__(self, init_info):
        self._next_subtask = _no_subtask
        self._subtask_iter = iter([])

    def is_task_done(self):
        if self._next_subtask is self._consumed_subtask:
            self._next_subtask = next(self._subtask_iter, self._no_subtask)
        return self._next_subtask is self._no_subtask

    def update(self):
        # Assumes executor always calls is_task_done to prepare next task before calling update
        subtask = self._next_subtask
        self._next_subtask = self._consumed_subtask
        return subtask

    def _submit_subtask_queue(self, queue):
        """Submits the queue of subtasks that the layer will emit each call to update.

        Call this method from accept_task or __init__ with an iterable of subtasks generated from
        the accepted task.
        Positional parameters:
        queue -- the iterable of subtasks to gradually emit after every update
        """
        self._subtask_iter = iter(queue)
        self._next_subtask = _consumed_subtask


class LayerSetupInfo:
    """Contains the information needed to initialize a layer."""

    def __init__(self, robot, robot_controller):
        """Creates a LayerSetupInfo.

        Positional arguments:
        robot -- the Robot or Robot-like object the layer may use to communicate with hardware
        robot_controller -- the RobotController that will run the layer
        """
        self._robot = robot
        self._robot_controller = robot_controller

    def get_robot(self):
        """Returns the Robot or Robot-like object used to communicate with hardware."""
        return self._robot

    def add_update_listener(listener):
        """Registers a function to be called on every update of the owning RobotController."""
        self._robot_controller.add_update_listener(listener)
