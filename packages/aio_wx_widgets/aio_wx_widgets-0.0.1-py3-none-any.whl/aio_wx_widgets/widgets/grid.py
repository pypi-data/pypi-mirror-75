"""Grid layout item."""

# pylint: disable=duplicate-code


import logging

import wx

from aio_wx_widgets.panels.panel import _add

_LOGGER = logging.getLogger(__name__)

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL


class Grid(wx.BoxSizer):
    """A grid component.

    Basically a boxsizer with some defaults.
    """

    default_sizer_margin = 0

    def __init__(self, orientation=HORIZONTAL):
        """Init."""
        self.parent = None
        self._box_sizer = None
        super().__init__(orient=orientation)

    def __call__(self, parent):
        self.parent = parent
        # self._box_sizer = wx.BoxSizer()
        return self

    # pylint: disable=duplicate-code
    def add(
        self,
        item,
        weight=1,
        layout=wx.EXPAND | wx.LEFT | wx.RIGHT,
        margin=None,
        create=True,
    ):
        """Add a UI component to this UI container."""
        return _add(
            item,
            self.parent,
            self,
            weight,
            layout,
            margin,
            self.default_sizer_margin,
            create,
        )

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
