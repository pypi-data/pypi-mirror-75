"""The HackerLab 9000 Overmind API server launcher."""

from hal9k_api.api import app


def main():
    """Start the HackerLab 9000 Overmind API server."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
