# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Union, NewType, Optional

from attr import dataclass

from mautrix.api import JSON
from ..primitive import RoomID, EventID, UserID
from ..util import deserializer, Obj, SerializableAttrs
from .base import EventType, BaseEvent
from .redaction import RedactionEvent, RedactionEventContent
from .message import MessageEvent, MessageEventContent
from .reaction import ReactionEvent, ReactionEventContent
from .encrypted import EncryptedEvent, EncryptedEventContent
from .state import StateEvent, StateEventContent
from .account_data import AccountDataEvent, AccountDataEventContent
from .ephemeral import (ReceiptEvent, PresenceEvent, TypingEvent, ReceiptEventContent,
                        TypingEventContent)


@dataclass
class GenericEvent(BaseEvent, SerializableAttrs['GenericEvent']):
    """
    An event class that contains all possible top-level event keys and uses generic Obj's for object
    keys (content and unsigned)
    """
    content: Obj
    type: EventType
    room_id: Optional[RoomID] = None
    event_id: Optional[EventID] = None
    sender: Optional[UserID] = None
    timestamp: Optional[int] = None
    state_key: Optional[str] = None
    unsigned: Obj = None
    readacts: Optional[EventID] = None


Event = NewType("Event", Union[MessageEvent,ReactionEvent, RedactionEvent, StateEvent, ReceiptEvent,
                               PresenceEvent, TypingEvent, EncryptedEvent, GenericEvent])

EventContent = Union[MessageEventContent, RedactionEventContent, ReactionEventContent,
                     StateEventContent, AccountDataEventContent, ReceiptEventContent,
                     TypingEventContent, EncryptedEventContent, Obj]


@deserializer(Event)
def deserialize_event(data: JSON) -> Event:
    event_type = EventType.find(data.get("type", None))
    if event_type == EventType.ROOM_MESSAGE:
        return MessageEvent.deserialize(data)
    elif event_type == EventType.STICKER:
        data.get("content", {})["msgtype"] = "m.sticker"
        return MessageEvent.deserialize(data)
    elif event_type == EventType.REACTION:
        return ReactionEvent.deserialize(data)
    elif event_type == EventType.ROOM_REDACTION:
        return RedactionEvent.deserialize(data)
    elif event_type.is_state:
        return StateEvent.deserialize(data)
    elif event_type.is_account_data:
        return AccountDataEvent.deserialize(data)
    elif event_type == EventType.RECEIPT:
        return ReceiptEvent.deserialize(data)
    elif event_type == EventType.TYPING:
        return TypingEvent.deserialize(data)
    elif event_type == EventType.PRESENCE:
        return PresenceEvent.deserialize(data)
    elif event_type == EventType.ROOM_ENCRYPTED:
        return EncryptedEvent.deserialize(data)
    else:
        return GenericEvent.deserialize(data)


setattr(Event, "deserialize", deserialize_event)
