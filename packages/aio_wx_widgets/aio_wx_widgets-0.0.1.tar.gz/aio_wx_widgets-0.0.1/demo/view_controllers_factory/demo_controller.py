import logging
from random import randint

from aio_wx_widgets.controller import BaseController
from demo.windows import second_window

_LOGGER = logging.getLogger(__name__)


class DemoController(BaseController):
    def __init__(self, model):
        self.value_1: int = 0
        self.a_string_value = "A certain string"
        super().__init__(model)

    async def open_other_window(self):
        """Open a second window."""
        _second_window = second_window.SecondWindow()
        _second_window.Show()

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.value_1 = val
