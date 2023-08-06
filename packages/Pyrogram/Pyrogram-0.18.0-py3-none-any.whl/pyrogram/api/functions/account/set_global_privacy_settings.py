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


class SetGlobalPrivacySettings(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0x1edaaac2``

    Parameters:
        settings: :obj:`GlobalPrivacySettings <pyrogram.api.types.GlobalPrivacySettings>`

    Returns:
        :obj:`GlobalPrivacySettings <pyrogram.api.types.GlobalPrivacySettings>`
    """

    __slots__ = ["settings"]

    ID = 0x1edaaac2
    QUALNAME = "functions.account.SetGlobalPrivacySettings"

    def __init__(self, *, settings):
        self.settings = settings  # GlobalPrivacySettings

    @staticmethod
    def read(b: BytesIO, *args) -> "SetGlobalPrivacySettings":
        # No flags
        
        settings = TLObject.read(b)
        
        return SetGlobalPrivacySettings(settings=settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.settings.write())
        
        return b.getvalue()
