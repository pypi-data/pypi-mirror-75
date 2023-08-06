"""
Main module of the server file
"""

import os

from flask import Response
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .validators import RequestBodyValidator

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CONFIGURATION_DIRECTORY = "openapi"
DB_FILE_NAME = "sqlite3.db"

# basedir points to the directory the program is running in.
SPECIFICATION_DIR = os.path.join(BASE_DIR, CONFIGURATION_DIRECTORY)  # i.e. <current_dir>/openapi

PG_USER = "postgres"
PG_PASSWORD = "postgres"
PG_PORT = 5432
PG_DATABASE_URI = "postgresql://{username}:{password}" \
                  "@localhost:{port}/flask_testing".format(username=PG_USER,
                                                           password=PG_PASSWORD,
                                                           port=PG_PORT)
SQLITE_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, DB_FILE_NAME)


def create_app(db_uri=SQLITE_DATABASE_URI):
    # Create the Connexion application instance
    _connexion_app = connexion.App(__name__, specification_dir=SPECIFICATION_DIR)

    # Get the underlying Flask app instance
    _app = _connexion_app.app  # Flask instance initialized by Connexion

    # Configure the SQLAlchemy part of the app instance
    _app.config["SQLALCHEMY_ECHO"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return _app, _connexion_app


# Get the application instance
_, connexion_app = create_app()

app = connexion_app.app  # Flask instance initialized by Connexion

DB = SQLAlchemy(app)
DB.create_all()

MA = Marshmallow(app)

# Read the specification.yml file to configure the endpoints
connexion_app.add_api("specification.yaml",
                      # strict_validation=True
                      validator_map={"body": RequestBodyValidator},
                      )


# create a URL route in our application for "/"
@connexion_app.route("/")
def home():
    return Response("Welcome to homepage.")


if __name__ == "__main__":
    connexion_app.run(debug=True)
