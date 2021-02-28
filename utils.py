def format_room_message(message: dict):
    format_message = message.copy()
    format_message['time'] = format_message['time'].strftime("%Y-%m-%d %H:%M:%S")
    return format_message
