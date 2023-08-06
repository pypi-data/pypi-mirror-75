import logging

from aio_wx_widgets.binding import Binding
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.button import async_button
from aio_wx_widgets.widgets.grid import Grid, VERTICAL
from aio_wx_widgets.widgets.group import Group
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import IntEntry, Entry
from demo.view_controllers_factory.demo_controller import DemoController

_LOGGER = logging.getLogger(__name__)


class DemoView(SimplePanel):
    def __init__(self, parent, controller: "DemoController"):
        self._controller = controller
        super().__init__(parent)

    def populate(self):
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
        self.add(Entry(binding=Binding(self._controller, "a_string_value")))
        self.add(Entry(binding=Binding(self._controller, "a_string_value")))

        with self.add(Grid()) as grd:
            grd.add(async_button("button one", self._set_value), weight=6)
            grd.add(async_button("button two,self", self._set_value), weight=6)

        with self.add(Grid()) as grd:
            grd.add(Text(text="A text"), weight=6, margin=2)
            with grd.add(Grid(VERTICAL), weight=6) as vert_grid:
                vert_grid.add(async_button("button two,self", self._set_value))
                vert_grid.add(async_button("button two,self", self._set_value))

        with self.add(Group("This is a group of controlls")) as grp:
            grp.add(async_button("button one", self._set_value))
        self.add(async_button("open other window", self._on_close))
        self.add(async_button("set value", self._set_value))

    async def _on_close(self, evt):
        await self._controller.open_other_window()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _set_value(self, evt):
        await self._controller.set_value()


class DemoViewOne(SimplePanel):
    def __init__(self, parent, controller: "DemoController"):
        self._controller = controller
        super().__init__(parent)

    def populate(self):
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
