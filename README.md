# curvy-potato

SIGN project

It uses **Flask/Flask-Restplus** for the server and **SQLAlchemy** as ORM with it GIS extension **GeoAlchemy2**.

## Quick start

First you need to create an environment file `.env` in the project root folder as follow:

```bash
DEBUG=False # True for debug
DATABASE_URI='dialect+driver://username:password@host:port/database'
# Uncomment the line bellow to fix an application key (eg. uuid)
# SECRET_KEY='secret_app_key'
```

If you do not specify an application secret key, a random key is used when the server starts.

You must install the required dependencies with `pip install -r Requirements.txt` (we recommend using a [virtual environment](https://virtualenv.pypa.io/en/stable/)).

You can now start playing with the API by starting it with `python manage.py runserver` and going to <http://127.0.0.1:5000/v1/>

## How to use

To interact with the project, you need to use the command line interface (`flask`). The main commands are listed bellow but it can be outdated, we recommend to read the help from the command.

| Command           |  description                                                       |
| :---------------- | :----------------------------------------------------------------- |
| runserver         | Start the development server.                                      |
| db --init         | Initialize the database.                                           |
| db --delete       | Delete the database.                                               |
| app add _name_    | Add a new application that can use the API. (Generate an API key.) |
| app delete _name_ | Delete an application.                                             |

## API

The API was documented with swagger. You can access it at <http://127.0.0.1:5000/v1/>
