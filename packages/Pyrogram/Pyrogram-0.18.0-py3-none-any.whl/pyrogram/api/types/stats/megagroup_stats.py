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


class MegagroupStats(TLObject):
    """Attributes:
        LAYER: ``116``

    Attributes:
        ID: ``0xef7ff916``

    Parameters:
        period: :obj:`StatsDateRangeDays <pyrogram.api.types.StatsDateRangeDays>`
        members: :obj:`StatsAbsValueAndPrev <pyrogram.api.types.StatsAbsValueAndPrev>`
        messages: :obj:`StatsAbsValueAndPrev <pyrogram.api.types.StatsAbsValueAndPrev>`
        viewers: :obj:`StatsAbsValueAndPrev <pyrogram.api.types.StatsAbsValueAndPrev>`
        posters: :obj:`StatsAbsValueAndPrev <pyrogram.api.types.StatsAbsValueAndPrev>`
        growth_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        members_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        new_members_by_source_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        languages_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        messages_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        actions_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        top_hours_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        weekdays_graph: Either :obj:`StatsGraphAsync <pyrogram.api.types.StatsGraphAsync>`, :obj:`StatsGraphError <pyrogram.api.types.StatsGraphError>` or :obj:`StatsGraph <pyrogram.api.types.StatsGraph>`
        top_posters: List of :obj:`StatsGroupTopPoster <pyrogram.api.types.StatsGroupTopPoster>`
        top_admins: List of :obj:`StatsGroupTopAdmin <pyrogram.api.types.StatsGroupTopAdmin>`
        top_inviters: List of :obj:`StatsGroupTopInviter <pyrogram.api.types.StatsGroupTopInviter>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`stats.GetMegagroupStats <pyrogram.api.functions.stats.GetMegagroupStats>`.
    """

    __slots__ = ["period", "members", "messages", "viewers", "posters", "growth_graph", "members_graph", "new_members_by_source_graph", "languages_graph", "messages_graph", "actions_graph", "top_hours_graph", "weekdays_graph", "top_posters", "top_admins", "top_inviters", "users"]

    ID = 0xef7ff916
    QUALNAME = "types.stats.MegagroupStats"

    def __init__(self, *, period, members, messages, viewers, posters, growth_graph, members_graph, new_members_by_source_graph, languages_graph, messages_graph, actions_graph, top_hours_graph, weekdays_graph, top_posters: list, top_admins: list, top_inviters: list, users: list):
        self.period = period  # StatsDateRangeDays
        self.members = members  # StatsAbsValueAndPrev
        self.messages = messages  # StatsAbsValueAndPrev
        self.viewers = viewers  # StatsAbsValueAndPrev
        self.posters = posters  # StatsAbsValueAndPrev
        self.growth_graph = growth_graph  # StatsGraph
        self.members_graph = members_graph  # StatsGraph
        self.new_members_by_source_graph = new_members_by_source_graph  # StatsGraph
        self.languages_graph = languages_graph  # StatsGraph
        self.messages_graph = messages_graph  # StatsGraph
        self.actions_graph = actions_graph  # StatsGraph
        self.top_hours_graph = top_hours_graph  # StatsGraph
        self.weekdays_graph = weekdays_graph  # StatsGraph
        self.top_posters = top_posters  # Vector<StatsGroupTopPoster>
        self.top_admins = top_admins  # Vector<StatsGroupTopAdmin>
        self.top_inviters = top_inviters  # Vector<StatsGroupTopInviter>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "MegagroupStats":
        # No flags
        
        period = TLObject.read(b)
        
        members = TLObject.read(b)
        
        messages = TLObject.read(b)
        
        viewers = TLObject.read(b)
        
        posters = TLObject.read(b)
        
        growth_graph = TLObject.read(b)
        
        members_graph = TLObject.read(b)
        
        new_members_by_source_graph = TLObject.read(b)
        
        languages_graph = TLObject.read(b)
        
        messages_graph = TLObject.read(b)
        
        actions_graph = TLObject.read(b)
        
        top_hours_graph = TLObject.read(b)
        
        weekdays_graph = TLObject.read(b)
        
        top_posters = TLObject.read(b)
        
        top_admins = TLObject.read(b)
        
        top_inviters = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return MegagroupStats(period=period, members=members, messages=messages, viewers=viewers, posters=posters, growth_graph=growth_graph, members_graph=members_graph, new_members_by_source_graph=new_members_by_source_graph, languages_graph=languages_graph, messages_graph=messages_graph, actions_graph=actions_graph, top_hours_graph=top_hours_graph, weekdays_graph=weekdays_graph, top_posters=top_posters, top_admins=top_admins, top_inviters=top_inviters, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.period.write())
        
        b.write(self.members.write())
        
        b.write(self.messages.write())
        
        b.write(self.viewers.write())
        
        b.write(self.posters.write())
        
        b.write(self.growth_graph.write())
        
        b.write(self.members_graph.write())
        
        b.write(self.new_members_by_source_graph.write())
        
        b.write(self.languages_graph.write())
        
        b.write(self.messages_graph.write())
        
        b.write(self.actions_graph.write())
        
        b.write(self.top_hours_graph.write())
        
        b.write(self.weekdays_graph.write())
        
        b.write(Vector(self.top_posters))
        
        b.write(Vector(self.top_admins))
        
        b.write(Vector(self.top_inviters))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
