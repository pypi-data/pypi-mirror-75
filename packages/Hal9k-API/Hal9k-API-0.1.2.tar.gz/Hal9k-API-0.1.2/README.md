# Hal9k-Overmind-API
The HackerLab 9000 Overmind API server.

## What is Hal9k-Overmind-API?
This is a back-end server designed to provide HTTP API access to the [HackerLab 9000 Library](https://github.com/haxys-labs/Lib-Hal9k).

## Future Goals
In the future, this API will include the ability to set up playlists, user authentication, access control, and more. The end goal is to create an API capable of being integrated with any number of front-end systems.

## Installation

`pip install Hal9k-API`

_Note: This requires the VirtualBox SDK to be properly installed and configured. Instructions will be added to this repository soon._

## Usage

To start the API server:

`python3 -m hal9k_api`

The API runs in debug mode on port 5000. It's accessible via HTTP methods:

```
haxys@straylight:~$ curl -X GET http://localhost:5000/
This is the HackerLab 9000 Overmind API Server. For more information, see <a href='https://github.com/haxys-labs/Hal9k-Overmind-API'>the GitHub repository</a>.
haxys@straylight:~$ curl -X GET http://localhost:5000/get_tracks/
{"tracks": ["Kali 2020.2 x64", "Debian 9.11 x64"]}
```

# Changelog

* **0.1.2** :: Refactored code; API remains consistent.
* **0.1.1** :: Fixed some minor bugs.
* **0.1.0** :: Implemented `get_tracks` functionality.
