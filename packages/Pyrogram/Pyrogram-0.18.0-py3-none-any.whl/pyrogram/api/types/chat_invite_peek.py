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


class ChatInvitePeek(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0x61695cb0``

    Parameters:
        chat: Either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        expires: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.CheckChatInvite <pyrogram.api.functions.messages.CheckChatInvite>`.
    """

    __slots__ = ["chat", "expires"]

    ID = 0x61695cb0
    QUALNAME = "types.ChatInvitePeek"

    def __init__(self, *, chat, expires: int):
        self.chat = chat  # Chat
        self.expires = expires  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatInvitePeek":
        # No flags
        
        chat = TLObject.read(b)
        
        expires = Int.read(b)
        
        return ChatInvitePeek(chat=chat, expires=expires)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        b.write(Int(self.expires))
        
        return b.getvalue()
