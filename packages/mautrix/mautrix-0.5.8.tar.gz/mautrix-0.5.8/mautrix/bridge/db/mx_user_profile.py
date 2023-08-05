# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Optional, Iterable

from sqlalchemy import Column, String, Enum

from mautrix.types import RoomID, UserID, ContentURI, Member, Membership
from mautrix.util.db import Base


class UserProfile(Base):
    __tablename__ = "mx_user_profile"

    room_id: RoomID = Column(String(255), primary_key=True)
    user_id: UserID = Column(String(255), primary_key=True)
    membership: Membership = Column(Enum(Membership), nullable=False, default=Membership.LEAVE)
    displayname: str = Column(String, nullable=True)
    avatar_url: ContentURI = Column(String(255), nullable=True)

    def member(self) -> Member:
        return Member(membership=self.membership, displayname=self.displayname,
                      avatar_url=self.avatar_url)

    @classmethod
    def get(cls, room_id: RoomID, user_id: UserID) -> Optional['UserProfile']:
        return cls._select_one_or_none((cls.c.room_id == room_id) & (cls.c.user_id == user_id))

    @classmethod
    def all_except(cls, prefix: str, suffix: str, bot: str) -> Iterable['UserProfile']:
        return cls._select_all(~(cls.c.user_id.startswith(prefix, autoescape=True)
                                 & cls.c.user_id.endswith(suffix, autoescape=True)
                                 & (cls.c.user_id != bot))
                               & ((cls.c.membership == Membership.JOIN)
                                  | (cls.c.membership == Membership.INVITE)))

    @classmethod
    def delete_all(cls, room_id: RoomID) -> None:
        with cls.db.begin() as conn:
            conn.execute(cls.t.delete().where(cls.c.room_id == room_id))
