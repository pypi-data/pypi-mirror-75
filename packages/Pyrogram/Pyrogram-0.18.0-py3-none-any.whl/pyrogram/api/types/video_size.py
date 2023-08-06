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


class VideoSize(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0xe831c556``

    Parameters:
        type: ``str``
        location: :obj:`FileLocationToBeDeprecated <pyrogram.api.types.FileLocationToBeDeprecated>`
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
        size: ``int`` ``32-bit``
        video_start_ts (optional): ``float`` ``64-bit``
    """

    __slots__ = ["type", "location", "w", "h", "size", "video_start_ts"]

    ID = 0xe831c556
    QUALNAME = "types.VideoSize"

    def __init__(self, *, type: str, location, w: int, h: int, size: int, video_start_ts: float = None):
        self.type = type  # string
        self.location = location  # FileLocation
        self.w = w  # int
        self.h = h  # int
        self.size = size  # int
        self.video_start_ts = video_start_ts  # flags.0?double

    @staticmethod
    def read(b: BytesIO, *args) -> "VideoSize":
        flags = Int.read(b)
        
        type = String.read(b)
        
        location = TLObject.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        size = Int.read(b)
        
        video_start_ts = Double.read(b) if flags & (1 << 0) else None
        return VideoSize(type=type, location=location, w=w, h=h, size=size, video_start_ts=video_start_ts)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.video_start_ts is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.type))
        
        b.write(self.location.write())
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        b.write(Int(self.size))
        
        if self.video_start_ts is not None:
            b.write(Double(self.video_start_ts))
        
        return b.getvalue()
