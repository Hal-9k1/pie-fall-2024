from abc import ABCMeta, abstractmethod


class Layer(metaclass=ABCMeta):
    """The base class of all layers.

    A layer is a modular unit of robot functionality. They interact with other layers by accepting
    tasks from the above layer and submitting tasks to the below layer. This represents the breaking
    down of a complex or abstract task into more simple and concrete ones.
    (A task is an instruction passed from a layer to its subordinate. Tasks range widely in their
    concreteness and can be as vague as "win the game" or as specific as "move forward 2 meters.")
    """

    @abstractmethod
    def is_task_done():
        """Returns whether the layer is ready to accept a new task.

        Returns True if the layer has finished processing the last accepted task, if any.
        """
        raise NotImplemented

    @abstractmethod
    def update():
        """Returns the next subordinate task produced from this layer's current task.

        Calculates the next subordinate task that should be submitted to the below layer. The return
        value of a bottom layer's update function is not used.
        """
        raise NotImplemented

    @abstractmethod
    def accept_task(task):
        """Sets the layer's current task.

        Accepts a task from the above layer. Should only be called after is_task_done() returns
        True.
        """
        raise NotImplemented


class TeleopLayer(Layer):
    """The base class of non-input-generating teleop layers.

    Layers used in the teleop robot mode should always present as done because they must accept a
    new "task" every update. The input generator at the top layer should always be asked for a new
    task.
    This class should not be the base of input generating layers, which should never present as
    done.
    """

    def is_task_done(self):
        return True


class InputGenerator(Layer):
    """The base class of input generating teleop layers.

    Input generators will be asked for a new task every robot update. This task should be to process
    the just-captured user input stored. Input generating layers must never present as done, which
    would prevent the layer and everything below it from ever again being updated by the controller
    in the likely case that the input generator is the top layer.
    """

    def is_task_done(self):
        return False
