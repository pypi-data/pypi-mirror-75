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


class UserProfilePhoto(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0x69d3ab26``

    Parameters:
        photo_id: ``int`` ``64-bit``
        photo_small: :obj:`FileLocationToBeDeprecated <pyrogram.api.types.FileLocationToBeDeprecated>`
        photo_big: :obj:`FileLocationToBeDeprecated <pyrogram.api.types.FileLocationToBeDeprecated>`
        dc_id: ``int`` ``32-bit``
        has_video (optional): ``bool``

    See Also:
        This object can be returned by :obj:`photos.UpdateProfilePhoto <pyrogram.api.functions.photos.UpdateProfilePhoto>`.
    """

    __slots__ = ["photo_id", "photo_small", "photo_big", "dc_id", "has_video"]

    ID = 0x69d3ab26
    QUALNAME = "types.UserProfilePhoto"

    def __init__(self, *, photo_id: int, photo_small, photo_big, dc_id: int, has_video: bool = None):
        self.has_video = has_video  # flags.0?true
        self.photo_id = photo_id  # long
        self.photo_small = photo_small  # FileLocation
        self.photo_big = photo_big  # FileLocation
        self.dc_id = dc_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UserProfilePhoto":
        flags = Int.read(b)
        
        has_video = True if flags & (1 << 0) else False
        photo_id = Long.read(b)
        
        photo_small = TLObject.read(b)
        
        photo_big = TLObject.read(b)
        
        dc_id = Int.read(b)
        
        return UserProfilePhoto(photo_id=photo_id, photo_small=photo_small, photo_big=photo_big, dc_id=dc_id, has_video=has_video)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.has_video is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.photo_id))
        
        b.write(self.photo_small.write())
        
        b.write(self.photo_big.write())
        
        b.write(Int(self.dc_id))
        
        return b.getvalue()
