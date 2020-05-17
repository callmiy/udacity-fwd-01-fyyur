import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = (
    "postgresql://udacity@:5431/fyyur?"
    "host=/home/kanmii/.asdf/installs/postgres/12.2/data/tmp/"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
