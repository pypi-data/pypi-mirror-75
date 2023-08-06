"""Panel. Sits in a frame. Holds widgets."""

import logging

import wx

_LOGGER = logging.getLogger(__name__)


def _add(item, parent, sizer, weight, layout, margin, default_margin, create) -> object:
    if margin is None:
        margin = default_margin
    if create:
        item = item(parent)

    sizer.Add(item, weight, layout, margin)

    return item


class SimplePanel(wx.Panel):
    """A simple panel."""

    default_sizer_margin = 5

    def __init__(self, parent):
        """Init."""

        super().__init__(parent)
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

    def add(self, item, weight=0, layout=wx.EXPAND | wx.ALL, margin=None, create=True):
        """Add an item to this panel"""
        return _add(
            item,
            self,
            self._sizer,
            weight,
            layout,
            margin,
            SimplePanel.default_sizer_margin,
            create,
        )

    def populate(self):
        """Add and configure widgets here."""
