# Introduction

This is a Django application which opens an API to play tic-tac-toe.


# Setup

### Installation

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

### Endpoints

* Separated dev and production settings


# Tests

The test suite can be run with:

```
python manage.py test
```