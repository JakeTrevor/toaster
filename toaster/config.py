import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = config("DEBUG", default=False, cast=bool)

if DEBUG:
    print("debug mode activated")
    DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "../sqlite.db")
else:
    DATABASE_URL = config("DATABASE_URL")

TOKEN = config("TOKEN")

COMMAND = config("COMMAND")
