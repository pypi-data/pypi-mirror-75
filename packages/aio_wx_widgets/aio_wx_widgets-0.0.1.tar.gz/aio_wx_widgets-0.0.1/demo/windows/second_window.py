import logging

from aio_wx_widgets.frame import DefaultFrame
from demo.view_controllers_factory import factory

_LOGGER = logging.getLogger(__name__)

class DemoModel:
    pass


class SecondWindow(DefaultFrame):
    def __init__(self):
        super().__init__("second window")

        model = DemoModel()
        view,controller = factory.get_demo_controller_one(self,model)

        self.add(controller.view,create=False)
