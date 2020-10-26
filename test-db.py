import psycopg2
import json


with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)


if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        database="vlad",
        user="vlad",
        password="mypassword",
        port="5432"
    )

    cur = conn.cursor()

    command = """
                CREATE TABLE IF NOT EXISTS players_masteries (
                    id SERIAL PRIMARY KEY,\n"""
    for champion_id in CHAMPIONS_NAMES:
        command += '                    ' + CHAMPIONS_NAMES[champion_id] + ' INTEGER,\n'
    command = command[:-2]+'\n                )'
    cur.execute(command)

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS challenger_players (
        id SERIAL PRIMARY KEY,
        summoner_name VARCHAR(20) NOT NULL,
        summoner_encrypt_id VARCHAR(63) NOT NULL,
        rank_order SMALLINT NOT NULL,
        region VARCHAR(5) NOT NULL,
        masteries_id INTEGER NOT NULL REFERENCES players_masteries (id)
    )
    """
    )

    cur.close()

    conn.commit()
    conn.close()

