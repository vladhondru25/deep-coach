import json
import datetime
import time
import sys

from resources.platform import *
from resources.region import *
from resources.database import *
from resources.riot-api import *


# CONSTANTS
MIN_CP = 200000 # Minimum threshold for champion points (200k)

# Read Champions Json
with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)


if __name__ == "__main__":
    # sys.exit()

    # Set up database
    db = Database()

    # Set up Riot API
    riot_client = Riot_API()

    # Get challenger players
    challenger_players = {}
    # Iterate through each platform
    for platform in PLATFORMS:
        decoded_players_json = riot_client.get_5x5_challengers(platform)
        if decoded_players_json != None:
            platform_players = {}
        
            # Get all the challenger players and their lp in the respective platform
            for player in decoded_players_json['entries']:
                platform_players[player['summonerName']] = player['leaguePoints']

            rank_counter = 1    # To get the rank in their league
            # Sort the players as a function of their lp and add them as a tuple to the dicitonary (key=platform)
            for p_name,p_lp in sorted(platform_players.items(), key=lambda item: item[1], reverse=True):
                temp_platform_players = challenger_players.get(platform, [])
                temp_platform_players.append( (p_name, p_lp, rank_counter) )
                challenger_players[platform] = temp_platform_players
                rank_counter += 1

    platform_dict = PLATFORMS.copy()
    while len(challenger_players) > 0:
        to_delete = []

        for platform in platform_dict:
            if len(challenger_players[platform]) == 0:
                to_delete.append(platform)
            else:
                # Get first player 
                player = challenger_players[platform].pop(0)
                # Get summoner account details (encrypted Summoner Id)
                summoner = riot_client.get_summoner(platform, summoner_name=player[0])
                if summoner != None
                    # Get the masteries points for the player
                    champs_masteries = riot_client.get_champions_masteries(platform, summoner_name=player[0], summoner_id=summoner['id'])
                    if champs_masteries != None:
                        # Store champions with more than 200k points that were played in the last 3 weeks
                        mastery_points_table = {}
                        # Iterate though each champion to check masteries
                        for champ in champs_masteries:
                            # Consider only if 200k points were achieved
                            if champ['championPoints'] >= MIN_CP:
                                # Calculate the last time the champion was played by the player
                                last_time_played = datetime.date.today() - datetime.date.fromtimestamp(champ['lastPlayTime']/1000)
                                if last_time_played < datetime.timedelta(days=21):
                                    mastery_points_table[CHAMPIONS_NAMES[champ[championId]]] = champ['championPoints']
                        # Add masteries points in the database
                        if len(mastery_points_table) > 0:
                            mastery_row_id = db.add_masteries_row(mastery_points_table)
                        # Add player to database
                        db.add_player_row((player[0], summoner['id'], player[2], platform, mastery_row_id))           

        for delete_platform in to_delete:
            del platform_dict[delete_platform]
            del challenger_players[delete_platform]

        # Insert waiting time below

    print('FINISH')
    sys.exit()

    

    with open('temp.json', 'w') as f:
        json.dump(challenger_players, f, indent=2)



    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="vlad",
    #     user="vlad",
    #     password="mypassword",
    #     port="5432"
    # )

    # cur = conn.cursor()

    # cur.execute(
    # """
    # CREATE TABLE IF NOT EXISTS challenger_players (
    #     id SERIAL PRIMARY KEY,
    #     summoner_name VARCHAR(20) NOT NULL,
    #     summoner_encrypt_id VARCHAR(63) NOT NULL,
    #     rank_order SMALLINT NOT NULL,
    #     region VARCHAR(5) NOT NULL
    # )
    # """
    # )
    # cur.close()

    # conn.commit()
    # conn.close()

