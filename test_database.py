import pytest
from database import create_new_room, create_message


def test_create_new_room():
    room_name = "test_room"
    room = create_new_room(room_name)
    assert room["name"] == room_name
    assert room["count_messages"] == 0


def test_create_message():
    room_name = "test_message"
    message_text = "test message for test message"
    room = create_new_room(room_name)
    message = create_message(room["room_id"], message_text)
    assert message["room_id"] == room["room_id"]
    assert message["message"] == message_text
