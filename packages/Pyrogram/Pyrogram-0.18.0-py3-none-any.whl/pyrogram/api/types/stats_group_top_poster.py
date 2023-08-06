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


class StatsGroupTopPoster(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0x18f3d0f7``

    Parameters:
        user_id: ``int`` ``32-bit``
        messages: ``int`` ``32-bit``
        avg_chars: ``int`` ``32-bit``
    """

    __slots__ = ["user_id", "messages", "avg_chars"]

    ID = 0x18f3d0f7
    QUALNAME = "types.StatsGroupTopPoster"

    def __init__(self, *, user_id: int, messages: int, avg_chars: int):
        self.user_id = user_id  # int
        self.messages = messages  # int
        self.avg_chars = avg_chars  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "StatsGroupTopPoster":
        # No flags
        
        user_id = Int.read(b)
        
        messages = Int.read(b)
        
        avg_chars = Int.read(b)
        
        return StatsGroupTopPoster(user_id=user_id, messages=messages, avg_chars=avg_chars)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.messages))
        
        b.write(Int(self.avg_chars))
        
        return b.getvalue()
