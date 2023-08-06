"""WX ui frames. A windows that holds a panel."""

import logging
from pathlib import Path
from typing import Optional

import wx

_LOGGER = logging.getLogger(__name__)


def _get_app_icon_32(img_path: Path):
    app_icon_32 = wx.Icon()
    app_icon_32.CopyFromBitmap(wx.Bitmap(str(img_path), wx.BITMAP_TYPE_PNG))
    return app_icon_32


class DefaultFrame(wx.Frame):
    """A default frame for app windows."""

    def __init__(
        self,
        title,
        parent=None,
        size: wx.Size = None,
        style=None,
        icon_img: Optional[Path] = None,
    ):
        """Init.

        Args:
            title:
            parent:
            size:
            style:
        """
        kwargs = {}
        if style is not None:
            kwargs["style"] = style

        if size is None:
            size = wx.Size(800, 600)

        kwargs["size"] = size
        kwargs["title"] = title

        wx.Frame.__init__(self, parent, **kwargs)
        if icon_img:
            self.SetIcon(_get_app_icon_32(icon_img))

        self._sizer = self._set_sizer()
        self.sizer_margin = 0

    def add_stretch_spacer(self, prop=1):
        """Add a stretch spacer to the current sizer."""
        self._sizer.AddStretchSpacer(prop=prop)

    def add(self, item, weight=0, layout=wx.EXPAND | wx.ALL, margin=None, create=True):
        """Add a ui component to this container."""
        args = [layout]

        if layout != wx.EXPAND:
            if margin is None:
                args.append(self.sizer_margin)
            else:
                args.append(margin)

        if create:
            item = item(self)
        self._sizer.Add(item, weight, *args)
        return item

    def _set_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        return sizer

    def fit_sizer(self):
        """Fit the sizer to the content."""
        self._sizer.Fit(self)
