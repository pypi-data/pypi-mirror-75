import json
import redis
import os
from flask import Flask, request
from typing import Text, Optional, Dict, Any


app = Flask(__name__)


def get_current_user() -> Optional[Dict[Text, Any]]:
    """Retrieve the current user from intermediate storage."""

    if os.environ.get("REDIS_HOST"):
        redis_url = os.environ.get("REDIS_HOST")
    else:
        redis_url = "redis"

    red = redis.StrictRedis(
        host=redis_url, port=6379, db=1, password=os.environ.get("REDIS_PASS", "abc123")
    )
    encoded_user = red.get("user")
    if encoded_user:
        return json.loads(encoded_user)
    else:
        return None


def store_user(user: Dict[Text, Any]) -> None:
    """Store a users details to our intermediate storage."""

    if os.environ.get("REDIS_HOST"):
        redis_url = os.environ.get("REDIS_HOST")
    else:
        redis_url = "redis"

    red = redis.StrictRedis(
        host=redis_url, port=6379, db=1, password=os.environ.get("REDIS_PASS", "abc123")
    )
    red.set("user", json.dumps(user))


@app.route("/", methods=["GET"])
def greet():
    """Send a welcoming message to the user."""

    user = get_current_user()
    if user is not None:
        return "Hello, {}!".format(user.get("name"))
    else:
        return "Hello, unknown stranger!"


@app.route("/", methods=["POST"])
def save_name():
    """Change a users details, most importantly his name."""

    user = request.json
    store_user(user)
    return "I'll try to remember your name, {}!".format(user.get("name"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=True)
