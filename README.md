# Healthy API

[![Build Status](https://img.shields.io/travis/com/Neplex/healthy-api/develop.svg)](https://travis-ci.com/Neplex/healthy-api)
[![Heroku](http://heroku-badge.herokuapp.com/?app=healthy-api-dev&svg=1&style=flat)](https://healthy-api-dev.herokuapp.com/)
[![CodeFactor](https://www.codefactor.io/repository/github/neplex/healthy-api/badge)](https://www.codefactor.io/repository/github/neplex/healthy-api)
![License](https://img.shields.io/github/license/Neplex/healthy-api.svg)


SIGN project

It uses **Flask/Flask-Restplus** for the server and **SQLAlchemy** as ORM with it GIS extension **GeoAlchemy2**.

## Quick start

First you need to create an environment file `.env` in the project root folder as follow:

```bash
DEBUG=False # True for debug
DATABASE_URL='dialect+driver://username:password@host:port/database'
# Uncomment the line bellow to fix an application key (eg. uuid)
# SECRET_KEY='secret_app_key'
```

If you do not specify an application secret key, a random key is used when the server starts.

You must install the required dependencies with `pip install -r requirements.txt` (we recommend using a [virtual environment](https://virtualenv.pypa.io/en/stable/)).

You can now start playing with the API by starting it with `flask run` and going to <http://127.0.0.1:5000/v1/>

## How to use

To interact with the project, you need to use the command line interface (`flask`). The main commands are listed bellow but it can be outdated, we recommend to read the help from the command.

| Command             |  Description                                                                 |
| :------------------ | :--------------------------------------------------------------------------- |
| run                 | Start the development server.                                                |
| database --init     | Initialize the database.                                                     |
| database --delete   | Delete the database.                                                         |
| database --populate | Populate the database (Add test user "string" "string" and some structures). |
| app add _name_      | Add a new application that can use the API. (Generate an API key.)           |
| app delete _name_   | Delete an application.                                                       |

## API

The API was documented with swagger. You can access it on heroku ([master](https://healthy-api-master.herokuapp.com/) or [develop](https://healthy-api-dev.herokuapp.com/) branch)

## Status

| Branch  | Build                                                                                                                         | Deploy                                                                                                           |
| :------ | :---------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------: |
| master  | [![Build Status](https://img.shields.io/travis/com/Neplex/healthy-api/master.svg)](https://travis-ci.com/Neplex/healthy-api)  | [![Heroku](http://heroku-badge.herokuapp.com/?app=healthy-api-master&svg=1&style=flat)](https://healthy-api-master.herokuapp.com/) |
| develop | [![Build Status](https://img.shields.io/travis/com/Neplex/healthy-api/develop.svg)](https://travis-ci.com/Neplex/healthy-api) | [![Heroku](http://heroku-badge.herokuapp.com/?app=healthy-api-dev&svg=1&style=flat)](https://healthy-api-dev.herokuapp.com/)       |
