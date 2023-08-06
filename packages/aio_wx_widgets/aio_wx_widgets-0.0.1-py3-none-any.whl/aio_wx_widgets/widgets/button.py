"""WX button."""

import logging
from asyncio import iscoroutinefunction
from typing import Callable, Any

import wx  # type: ignore
from wxasync import AsyncBind  # type: ignore

from aio_wx_widgets.colors import GREEN
from aio_wx_widgets.const import is_debugging

_LOGGER = logging.getLogger(__name__)


def async_button(label: str, callback: Callable[[Any], Any], parent=None):
    """Button with async binding."""
    btn = wx.Button()

    if is_debugging():
        btn.SetBackgroundColour(GREEN)

    def _create(parent: wx.Window):
        btn.Create(parent, -1, label=str(label))
        if iscoroutinefunction(callback):
            AsyncBind(wx.EVT_BUTTON, callback, btn)  # type: ignore
        else:
            parent.Bind(wx.EVT_BUTTON, callback, btn)
        return btn

    if parent is None:
        return _create

    return _create(parent)
