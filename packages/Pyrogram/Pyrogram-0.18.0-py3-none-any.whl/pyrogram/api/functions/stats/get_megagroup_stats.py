# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class GetMegagroupStats(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0xdcdf8607``

    Parameters:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>`, :obj:`InputChannel <pyrogram.api.types.InputChannel>` or :obj:`InputChannelFromMessage <pyrogram.api.types.InputChannelFromMessage>`
        dark (optional): ``bool``

    Returns:
        :obj:`stats.MegagroupStats <pyrogram.api.types.stats.MegagroupStats>`
    """

    __slots__ = ["channel", "dark"]

    ID = 0xdcdf8607
    QUALNAME = "functions.stats.GetMegagroupStats"

    def __init__(self, *, channel, dark: bool = None):
        self.dark = dark  # flags.0?true
        self.channel = channel  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args) -> "GetMegagroupStats":
        flags = Int.read(b)
        
        dark = True if flags & (1 << 0) else False
        channel = TLObject.read(b)
        
        return GetMegagroupStats(channel=channel, dark=dark)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark is not None else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        return b.getvalue()
