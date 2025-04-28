"Utilities for working with AI messages"


def _filter_part(message):
    for part in message.parts:
        if not hasattr(part, "content"):
            continue
        if hasattr(part.content[0], "kind") and part.content[0].kind.startswith(
            "binary"
        ):
            binary_content = part.content[0]
            part.content[0] = (
                f"{binary_content.media_type} size: {len(binary_content.data):,} bytes"
            )
    return message


def filter_messages(messages: list) -> list:
    """
    Filter out messaages that contain BinaryContent in order to avoid JSON serialization errors.
    Args:
        messages (list): List of messages to filter.
    Returns:
        list: Filtered list of messages.
    """
    filtered_messages = []
    for message in messages:
        if message.parts:
            message = _filter_part(message)
        filtered_messages.append(message)
    return filtered_messages
