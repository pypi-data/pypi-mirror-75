import logging
import pytest
from aio_wx_widgets.binding import Binding, Bindable, WATCHERS
from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)
#
# class SomeBinding(Binding):
#


class SomeController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.a_value = 10


@pytest.fixture
def some_controller(base_model):
    return SomeController(base_model)


@pytest.fixture
def some_binding(some_controller):
    return Binding(bound_object=some_controller, bound_property="a_value")


@pytest.fixture
def some_bindable(mocker, some_binding):
    mocker.patch.object(Bindable, "_get_ui_value")
    mocker.patch.object(Bindable, "_set_ui_value")

    return Bindable(some_binding)


def test_make_binding(some_bindable, some_controller):
    some_bindable._make_binding()

    # check if watcher is added to list of watchers.
    watchers = some_controller.__dict__[WATCHERS]["a_value"]
    assert len(watchers) == 1

    # Check if widget is updated with the default value.
    some_bindable._set_ui_value.assert_called_once_with(10)
