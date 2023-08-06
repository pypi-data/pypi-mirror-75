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


class StatsGroupTopAdmin(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0x6014f412``

    Parameters:
        user_id: ``int`` ``32-bit``
        deleted: ``int`` ``32-bit``
        kicked: ``int`` ``32-bit``
        banned: ``int`` ``32-bit``
    """

    __slots__ = ["user_id", "deleted", "kicked", "banned"]

    ID = 0x6014f412
    QUALNAME = "types.StatsGroupTopAdmin"

    def __init__(self, *, user_id: int, deleted: int, kicked: int, banned: int):
        self.user_id = user_id  # int
        self.deleted = deleted  # int
        self.kicked = kicked  # int
        self.banned = banned  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "StatsGroupTopAdmin":
        # No flags
        
        user_id = Int.read(b)
        
        deleted = Int.read(b)
        
        kicked = Int.read(b)
        
        banned = Int.read(b)
        
        return StatsGroupTopAdmin(user_id=user_id, deleted=deleted, kicked=kicked, banned=banned)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.deleted))
        
        b.write(Int(self.kicked))
        
        b.write(Int(self.banned))
        
        return b.getvalue()
