# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Dict, Tuple

from mautrix.types import UserID, RoomID, PowerLevelStateEventContent, Membership, Member
from mautrix.appservice import StateStore

from .mx_user_profile import UserProfile
from .mx_room_state import RoomState


class SQLStateStore(StateStore):
    _profile_cache: Dict[Tuple[RoomID, UserID], UserProfile]
    _room_state_cache: Dict[RoomID, RoomState]
    _registered: Dict[UserID, bool]

    def __init__(self) -> None:
        super().__init__()
        self._profile_cache = {}
        self._room_state_cache = {}
        self._registered = {}

    def is_registered(self, user_id: UserID) -> bool:
        if not user_id:
            raise ValueError("user_id is empty")
        return self._registered.get(user_id, False)

    def registered(self, user_id: UserID) -> None:
        if not user_id:
            raise ValueError("user_id is empty")
        self._registered[user_id] = True

    def _get_user_profile(self, room_id: RoomID, user_id: UserID, create: bool = True
                          ) -> UserProfile:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        key = (room_id, user_id)
        try:
            return self._profile_cache[key]
        except KeyError:
            pass

        profile = UserProfile.get(*key)
        if profile:
            self._profile_cache[key] = profile
        elif create:
            profile = UserProfile(room_id=room_id, user_id=user_id, membership=Membership.LEAVE)
            profile.insert()
            self._profile_cache[key] = profile
        return profile

    def get_member(self, room_id: RoomID, user_id: UserID) -> Member:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        return self._get_user_profile(room_id, user_id).member()

    def set_member(self, room_id: RoomID, user_id: UserID, member: Member) -> None:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        elif not member:
            raise ValueError("member info is empty")
        profile = self._get_user_profile(room_id, user_id)
        profile.edit(membership=member.membership,
                     displayname=member.displayname or profile.displayname,
                     avatar_url=member.avatar_url or profile.avatar_url)

    def set_membership(self, room_id: RoomID, user_id: UserID, membership: Membership) -> None:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        elif not membership:
            raise ValueError("membership is empty")
        self.set_member(room_id, user_id, Member(membership=membership))

    def _get_room_state(self, room_id: RoomID, create: bool = True) -> RoomState:
        try:
            return self._room_state_cache[room_id]
        except KeyError:
            pass

        room = RoomState.get(room_id)
        if room:
            self._room_state_cache[room_id] = room
        elif create:
            room = RoomState(room_id=room_id)
            room.insert()
            self._room_state_cache[room_id] = room
        return room

    def has_power_levels(self, room_id: RoomID) -> bool:
        if not room_id:
            raise ValueError("room_id is empty")
        return self._get_room_state(room_id).has_power_levels

    def get_power_levels(self, room_id: RoomID) -> PowerLevelStateEventContent:
        if not room_id:
            raise ValueError("room_id is empty")
        return self._get_room_state(room_id).power_levels

    def set_power_level(self, room_id: RoomID, user_id: UserID, level: int) -> None:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        room_state = self._get_room_state(room_id)
        power_levels = room_state.power_levels
        if not power_levels:
            power_levels = PowerLevelStateEventContent()
        power_levels.users[user_id] = level or 0
        room_state.edit(power_levels=power_levels)

    def set_power_levels(self, room_id: RoomID, content: PowerLevelStateEventContent) -> None:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not content:
            raise ValueError("content is empty")
        self._get_room_state(room_id).edit(power_levels=content)
