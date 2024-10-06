from dataclasses import dataclass
from layer import Layer

class UnsupportedTaskError(TypeError):
    """Exception raised by layers when accepting a task type they don't support."""

    def __init__(self, layer, task):
        super().__init__(f"Layer '{type(layer).__name__}' does not support task of type"
            f" '{type(task).__name__}'.")


@dataclass
class PrintTitleTask:
    text: str


@dataclass
class PrintItemTask:
    text: str


@dataclass
class SectionTask:
    title: str
    items: list[str]


class RestaurantPrinter(Layer):
    def __init__(self, init_info):
        pass

    def is_task_done(self):
        return True

    def update(self):
        if self._is_title:
            print(self._cur_text)
            print("-" * len(self._cur_text))
        else:
            print("    " + self._cur_text)

    def accept_task(self, task):
        if isinstance(task, PrintTitleTask):
            self._is_title = True
        elif isinstance(task, PrintItemTask):
            self._is_title = False
        else:
            raise UnsupportedTaskError(self, task)
        self._cur_text = task.text


class RestaurantSectionLayer(Layer):
    def __init__(self, init_info):
        self._next_print_task = None
        self._print_tasks = iter([])

    def is_task_done(self):
        if self._next_print_task is None:
            self._next_print_task = next(self._print_tasks, None)
        return self._next_print_task is None

    def update(self):
        # Generate next task if necessary. Shouldn't return None if caller called it before us
        self.is_task_done()
        task = self._next_print_task
        self._next_print_task = None
        return task

    def accept_task(self, task):
        if not isinstance(task, SectionTask):
            raise UnsupportedTaskError(self, task)
        self._print_tasks = iter([PrintTitleTask(text=task.title)]
            + [PrintItemTask(text=item) for item in task.items] + [PrintItemTask(text="")])


class RestaurantMenuSource(Layer):
    def __init__(self, init_info):
        self._next_section = None
        self._sections = iter([
            SectionTask(
                title="Breakfast",
                items=[
                    "Croissant",
                    "Danish",
                    "Cornbread muffin",
                    "Toast",
                    "Spam and eggs",
                ]
            ),
            SectionTask(
                title="Appetizers",
                items=[
                    "Finger sandwiches",
                    "Gorgonzola salad",
                    "Parmesan tomato soup",
                    "Breadsticks",
                    "Bell pepper medley",
                ]
            ),
            SectionTask(
                title="Entrees",
                items=[
                    "Spaghetti",
                    "Chicken noodle soup",
                    "Pizza",
                    "Pork stew",
                    "Tomato mozzarella sandwich",
                    "New York pizza",
                ]
            ),
            SectionTask(
                title="Dessert",
                items=[
                    "Rice pudding",
                    "Ice cream",
                    "Apple pie",
                    "Fruitcake",
                ]
            ),
            SectionTask(
                title="Drinks",
                items=[
                    "Mixed fruit juice",
                    "Mocha",
                    "Milk tea",
                    "Herbal tea",
                    "Espresso",
                ]
            ),
        ])


    def is_task_done(self):
        if self._next_section is None:
            self._next_section = next(self._sections, None)
        return self._next_section is None

    def update(self):
        self.is_task_done()
        section = self._next_section
        self._next_section = None
        return section

    def accept_task(self):
        raise TypeError("And who let you give orders to the chef huh??")
