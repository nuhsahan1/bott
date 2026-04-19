"""
Development and testing utilities.
"""
import json
from datetime import datetime

# Example Telegram update structure for testing
SAMPLE_TELEGRAM_UPDATE = {
    "update_id": 123456789,
    "message": {
        "message_id": 1,
        "from": {
            "id": 987654321,
            "is_bot": False,
            "first_name": "John",
            "username": "johndoe"
        },
        "chat": {
            "id": 987654321,
            "first_name": "John",
            "username": "johndoe",
            "type": "private"
        },
        "date": int(datetime.utcnow().timestamp()),
        "text": "Hello bot!"
    }
}


def print_sample_update():
    """Print sample Telegram update for testing."""
    print(json.dumps(SAMPLE_TELEGRAM_UPDATE, indent=2))


if __name__ == "__main__":
    print_sample_update()
