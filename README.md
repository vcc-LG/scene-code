# Introduction

This is a Django application which opens an API to play tic-tac-toe.


# Setup

## Installation

Clone this repo and change directory:
```sh
git clone https://github.com/vcc-LG/scene-code.git
cd scene-code
```

Install requirements:
```sh
pip install -r requirements.txt
```

Run migrations:
```sh
cd scene
python manage.py migrate
```

# Usage
Start the server using:
```sh
python manage.py runserver
```

Now when you browse to:

[http://localhost:8000/](http://localhost:8000/)

you should see a successful response from the server.

# Game rules

A Game has two players: `x` and `o`. Either player can go first, but the players **must** alternate.

The Game grid is a matrix of dimensions `3x3`. Each request to the API specifies the player and the coordinate where they wish to move. A player cannot make a move on a populated grid square. 

A Game is won when a player gets three in a horizontal, vertical, or diagonal row. A Game can also end in a draw.


# Endpoints

The base URL is:

[http://localhost:8000/tictactoe/api/](http://localhost:8000/tictactoe/api/)

No authentication is required to access the endpoints. 

## Games

- `POST /games` - Create a new Game
- `GET /games/<id>` - Retrieve a Game's information
- `DELETE /games/<id>` - Delete a Game

The `status` property of a Game can have the following values: `win`, `draw`, or `incomplete`. 

A Game with a status of `win` will have a property of `victor` which can have a value of `x` or `o`. 

## Move

- `POST /games/<id>/moves` - Create a new Move for a Game
- `GET /games/<id>/moves/<id>` - Retrieve a Move's information
- `DELETE /games/<id>/moves/<id>` - Delete a Move

If a move is illegal then the API will return a `400 Bad Request`.

If a move results in an end state, the API will return a JSON object with a `status` property, e.g.:
```json 
HTTP 200
{
    "id": <id>,
    "status": "win",
    "victor: "x"
}
```


# Tests

The test suite can be run with:

```
python manage.py test
```