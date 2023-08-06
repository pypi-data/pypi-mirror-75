"""MVC controller."""

import logging
from typing import TYPE_CHECKING, List, Optional

import wx

from aio_wx_widgets.binding import WATCHERS

if TYPE_CHECKING:
    from aiosubpub import Channel, Subscription

_LOGGER = logging.getLogger(__name__)


class BaseController:
    """Base implementation of a controller."""

    def __init__(self, model: object):
        """Init.

        Args:
            view: The view part.
            model: The model.
        """

        self.model = model
        self.view: Optional["wx.Panel"] = None

        self._subscriptions: List["Subscription"] = []

    def set_view(self, view: "wx.Panel"):
        """Finalize view creation."""
        self.view = view
        self.view.Bind(wx.EVT_WINDOW_DESTROY, self._on_close)
        self.view.Bind(wx.EVT_CLOSE, self._on_close)

    def __setattr__(self, item, value):
        print(f"Setting item {item} to value {value}")
        self.__dict__[item] = value
        if WATCHERS not in self.__dict__:
            return
        if item not in self.__dict__[WATCHERS]:
            return

        watchers = self.__dict__[WATCHERS][item]
        for watcher in watchers:
            watcher(value)

    def subscribe(self, channel: "Channel", callback):
        """Subscribe to a listener.

        On exit these listeners will be deleted.
        """

        subscription = channel.subscribe(callback)
        self._subscriptions.append(subscription)
        return subscription

    def _on_close(self, event):
        _LOGGER.debug("cancelling tasks in _channels.")
        for task in self._subscriptions:

            task.cancel()
        self._subscriptions = []

        event.Skip()
