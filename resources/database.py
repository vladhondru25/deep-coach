import psycopg2
import json


with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)


class Database:
    def __init__(self):
        # Connection
        self.conn = psycopg2.connect(
            host="localhost",
            database="vlad",
            user="vlad",
            password="mypassword",
            port="5432"
        )
        # Cursor
        self.cur = conn.cursor()

    def __del__(self): 
        self.cur.close()
        self.conn.close()

    def create_players_masteries_table(self):
        command = """
                CREATE TABLE IF NOT EXISTS players_masteries (
                    id SERIAL PRIMARY KEY,\n"""
        for champion_id in CHAMPIONS_NAMES:
            command += '                    ' + CHAMPIONS_NAMES[champion_id] + ' INTEGER,\n'
        command = command[:-2]+'\n                )'
        self.cur.execute(command)
        self.conn.commit()

    def create_challenger_players_table(self):
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
        self.conn.commit()

    def add_player_row(self, values):
        insert_query = """ INSERT INTO challenger_players (summoner_name, summoner_encrypt_id, rank_order, region, masteries_id) 
                           VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (*values)
        self.cur.execute(postgres_insert_query, record_to_insert)
        self.conn.commit()

    def add_masteries_row(self, mastery_points_table):
        insert_query = """ INSERT INTO players_masteries ("""
        no_of_s = ''
        for champ_name,_ in mastery_points_table:
            insert_query += champ_name + ', '
            no_of_s += '%s,'
        insert_query[-1] = ') ' # Eliminate last comma and add closing paranthesis
        no_of_s[-1] = ') '
        insert_query += 'VALUES (' + no_of_s
        insert_query += ' RETURNING id'

        record_to_insert = (*mastery_points_table.values())

        self.cur.execute(postgres_insert_query, record_to_insert)
        self.conn.commit()

        return self.cur.fetchone()[0]