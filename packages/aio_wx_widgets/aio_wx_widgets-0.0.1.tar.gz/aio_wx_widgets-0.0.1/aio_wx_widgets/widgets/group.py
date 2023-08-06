"""Group layout item. Draws a line around children and sets a title."""


import logging

import wx

from aio_wx_widgets.panels.panel import _add

_LOGGER = logging.getLogger(__name__)


class Group(wx.StaticBox):
    """A UI container."""

    default_sizer_margin = 20

    def __init__(self, label, parent=None):
        """Init.

        Args:
            label:
            parent:
        """
        self._label = label
        wx.StaticBox.__init__(self)
        self._extra_bottom_border = 10
        # if KEY_PLATFORM == KEY_LINUX:
        #     self._extra_bottom_border = 50
        self._parent = None
        if parent:
            self.__call__(parent)

    def __call__(self, parent):
        """Call this class as a function.

        Args:
            parent: The parent of this ui item.

        """
        self.Create(parent, label=self._label)
        self._sizer = wx.BoxSizer(wx.VERTICAL)

        top, other = self.GetBordersForSizer()
        self.bottom_border = other + self._extra_bottom_border
        # self.top_border=top
        self._sizer.AddSpacer(top)
        self.SetSizer(self._sizer)
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        self._finish()

    def _finish(self):
        self._sizer.AddSpacer(self.bottom_border)

    def add(
        self,
        item,
        weight=0,
        layout=wx.EXPAND | wx.LEFT | wx.RIGHT,
        margin=None,
        create=True,
    ):
        # pylint: disable=duplicate-code
        """Add a UI component to this UI container."""
        return _add(
            item,
            parent=self,
            sizer=self._sizer,
            weight=weight,
            layout=layout,
            margin=margin,
            default_margin=self.default_sizer_margin,
            create=create,
        )
