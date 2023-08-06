"""Property binding."""

import logging
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)

WATCHERS = "_watchers_"


class Binding(NamedTuple):
    """Binding data."""

    bound_object: "BaseController"
    bound_property: "str"


class Bindable:
    """Base class for binding a property to a widget.

    Make a widget inherit from this. The binding property modifies the controller bound
    property adding a watcher and emitting change events.
    """

    def __init__(self, binding: "Binding"):
        self._binding = binding

        # Flag to stop firing updates when a property value has changed.
        # Prevents infinite loop of updating the value and firing update events.
        self._fire_update_event = True

    def _make_binding(self):
        if WATCHERS not in self._binding.bound_object.__dict__:
            self._binding.bound_object.__dict__[WATCHERS] = {}
        if (
            self._binding.bound_property
            not in self._binding.bound_object.__dict__[WATCHERS]
        ):
            _LOGGER.debug("No watchers yet for %s", self._binding.bound_property)
            self._binding.bound_object.__dict__[WATCHERS][
                self._binding.bound_property
            ] = []
        self._binding.bound_object.__dict__[WATCHERS][
            self._binding.bound_property
        ].append(self._update)

        value = getattr(self._binding.bound_object, self._binding.bound_property)

        self._set_ui_value(value)

    def _set_property_value(self, value):
        setattr(self._binding.bound_object, self._binding.bound_property, value)

    def _update(self, value):
        """Called when a property changes from outside this control.

        Update the control with the new value
        """
        _LOGGER.debug("Updating entry with new value.")
        self._fire_update_event = False
        self._set_ui_value(value)

    def _on_ui_change(self, *args, **kwargs):
        """Callback when UI widget value changes by user input."""
        _LOGGER.debug("UI value changed")
        if self._fire_update_event:
            _LOGGER.debug("Firing update")
            val = self._get_ui_value()
            self._set_property_value(val)
        self._fire_update_event = True

    def _get_ui_value(self):
        """Get the value from the ui widget."""
        raise NotImplementedError()

    def _set_ui_value(self, value):
        raise NotImplementedError()
