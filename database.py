import os
import psycopg2
import psycopg2.extras
import datetime


def _open_db_connection():
    env_host = os.environ.get("BD_HOST")
    host = env_host if env_host is not None else "localhost"

    return psycopg2.connect(database="postgres", user="postgres",
                            password="s3cr3t", host=host, port=5432)


def create_new_room(room_name):
    db_connection = _open_db_connection()
    request_to_new_room = "INSERT INTO rooms (name) VALUES (%s) RETURNING room_id"
    with db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute(request_to_new_room, [room_name])
            room_id = db_cursor.fetchone()[0]
    db_connection.close()
    return {'room_id': room_id, 'name': room_name, 'count_messages': 0}


def get_all_rooms():
    db_connection = _open_db_connection()
    request_to_all_rooms = "SELECT rooms.room_id, rooms.name, count(messages.message_id) FROM rooms " \
                           "LEFT OUTER JOIN messages ON rooms.room_id=messages.room_id " \
                           "GROUP BY rooms.room_id ORDER BY rooms.room_id LIMIT 100"
    all_rooms = []
    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as db_cursor:
            db_cursor.execute(request_to_all_rooms)
            all_rooms = list(map(dict, db_cursor))
    db_connection.close()
    return all_rooms


def get_room_messages(room_id):
    db_connection = _open_db_connection()
    request_all_messages = "SELECT message_id, room_id, message, time FROM messages WHERE room_id = (%s) LIMIT 1000"
    room_messages = []
    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as db_cursor:
            db_cursor.execute(request_all_messages, [room_id])
            room_messages = list(map(dict, db_cursor))
    db_connection.close()
    return room_messages


def create_message(room_id, text):
    db_connection = _open_db_connection()
    request_to_new_message = "INSERT INTO messages (room_id, message, time) VALUES (%s, %s, %s) " + \
                             "RETURNING message_id, room_id, message, time"
    message_time = datetime.datetime.now(datetime.timezone.utc)
    new_message = None
    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as db_cursor:
            db_cursor.execute(request_to_new_message, [room_id, text, message_time])
            new_message = dict(db_cursor.fetchone())
    db_connection.close()
    return new_message


def delete_message(message_id):
    db_connection = _open_db_connection()
    request_to_new_message = "DELETE FROM messages WHERE message_id = (%s)"
    with db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute(request_to_new_message, [message_id])
    db_connection.close()
