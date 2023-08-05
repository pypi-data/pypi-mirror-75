"""The HackerLab 9000 Overmind API server library."""

import json

from flask import Flask
from flask_cors import CORS
from hal9k import Meta

app = Flask(__name__)
META = Meta()

# Warning: The following CORS settings allow for all routes from all domains!
# TODO: Configure this properly.
CORS(app, resources={r"/*": {"origins:": "*"}})


@app.route("/", methods=["GET"])
def index():
    """Return the index page."""
    return (
        "".join(
            [
                "This is the HackerLab 9000 Overmind API Server. For more ",
                "information, see <a href='https://github.com/haxys-labs/",
                "Hal9k-Overmind-API'>the GitHub repository</a>.",
            ]
        ),
        200,
    )


@app.route("/get_tracks/", methods=["GET"])
def get_tracks():
    """Return a listing of available tracks."""
    tracks = META.get_tracks()
    return json.dumps({"tracks": tracks}), 200
