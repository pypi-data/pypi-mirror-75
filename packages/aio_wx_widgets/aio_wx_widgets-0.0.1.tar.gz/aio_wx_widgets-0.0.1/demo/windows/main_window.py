import logging

from aio_wx_widgets.frame import DefaultFrame
from demo.view_controllers_factory.factory import get_demo_controller_view

_LOGGER = logging.getLogger(__name__)


class DemoModel:
    pass


class MainWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Main window")

        model = DemoModel()
        view, controller = get_demo_controller_view(self, model)
        self.add(controller.view, create=False)
