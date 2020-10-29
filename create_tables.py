import psycopg2
import json

from resources.database import *

if __name__ == "__main__":
    db = Database()

    db.create_players_masteries_table()
    db.create_challenger_players_table()

