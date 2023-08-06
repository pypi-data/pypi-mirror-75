"""Text widgets."""

import logging
from typing import Optional

import wx

from aio_wx_widgets.colors import GREEN
from aio_wx_widgets.const import is_debugging

_LOGGER = logging.getLogger(__name__)


class Text(wx.StaticText):
    """Static text."""

    def __init__(
        self, text="", font_size=None, color: Optional[int] = None, parent=None,
    ):
        """Init.

        Args:
            parent:
            text:
            font_size:
        """
        self._color = color
        self._text = text

        super().__init__()

        self._font_size = None
        if font_size:
            self._font_size = wx.Font(wx.FontInfo(font_size))

    def __call__(self, parent):
        self.Create(parent)
        if self._font_size:
            self.SetFont(self._font_size)
        self.set_text(self._text, self._color)
        if is_debugging():
            self.SetBackgroundColour(GREEN)
        return self

    def set_text(self, text, color=None):
        """Set text."""
        self._text = text
        self.SetLabel(self._text)
        if color:
            self.SetForegroundColour(color)
