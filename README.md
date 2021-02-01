# Introduction

This is a Django application which creates an open API to allow a user to play tic-tac-toe.


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

[http://localhost:8000/games/](http://localhost:8000/games/)

you should see an empty array displayed, indicating a successful response from the application.

# Game rules

A game has two players: `x` and `o`. Either player can go first, but the players must alternate.

The Game grid is a matrix of dimensions `3x3`:

| <!-- -->    | <!-- -->    |<!-- -->    |
|-------------|-------------|-------------|
| [0,0]         | [0,1]         | [0,2]        |
| [1,0]         | [1,1]         | [1,2]        |
| [2,0]         | [2,1]         | [2,2]        |
| <!-- -->    | <!-- -->    |<!-- -->    |

 The body of a request to the API to perform a move specifies the player and the coordinate where they wish to move. A player cannot make a move to a populated grid square or to a square outside the game grid.

A game is won when a player gets three in a horizontal, vertical, or diagonal row. A game can also end in a draw if all grid squares are populated with no victor.


# Endpoints

The base URL is:

[http://localhost:8000/games/](http://localhost:8000/games/)

No authentication is required to access the endpoints. 

## Games

- `GET /games/` - Retrieve all games
- `POST /games/` - Create a new game
- `GET /games/<game_id>/` - Retrieve a game's details
- `DELETE /games/<game_id>/` - Delete a game

The `status` property of a Game can have the following values: `win`, `draw`, or `incomplete`. A game is played by sending API requests to create moves.


## Move

- `GET /games/<game_id>/moves/` - Retrieve all moves for a game
- `POST /games/<game_id>/moves/` - Create a move for a game
- `GET /games/<game_id>/moves/<move_id>/` - Retrieve a move's details
- `DELETE /games/<game_id>/moves/<move_id>/` - Delete a move

Here is an example of a request to create a move:

`POST /games/1/moves/`
```
{
    "player": "o"
    "coord": [2,2]
}
```
Which would result in the following board:

| <!-- -->    | <!-- -->    |<!-- -->    |
|-------------|-------------|-------------|
| -         | -         | -         |
| -         | -         | -         |
| -         | -         | o         |
| <!-- -->    | <!-- -->    |<!-- -->    |


If a move is illegal then the API will return a `400 Bad Request` and a helpful error message.

# Tests

The test suite can be run with:

```
python manage.py test
```