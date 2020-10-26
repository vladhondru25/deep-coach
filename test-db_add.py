import psycopg2
import requests
import json
import datetime
import time
import sys

from resources.platform import *
from resources.region import *
from resources.database import *


# CONSTANTS
MIN_CP = 200000 # Minimum threshold for champion points (200k)

# Read Champions Json
with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)

# Read private key
with open('resources/MY_PRIVATE_KEY.txt') as pk_file:
    PRIVATE_KEY = pk_file.readline()

header = {
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9,ro;q=0.8",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": PRIVATE_KEY
}

if __name__ == "__main__":
    # sys.exit()

    # Set up database
    db = Database()

    # Get challenger players
    challenger_players = {}
    # Iterate through each platform
    for platform in PLATFORMS:
        req = requests.get(PLATFORMS[platform]+'/lol/league/v4/challengerleagues/by-queue/'+'RANKED_SOLO_5x5', headers=header)
        if req.status_code == 200:
            platform_players = {}
            decoded_players_json = json.loads(req.text)
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

        else:
            print('Request for challenger players in {} failed. Status code={}.'.format(platform, req.status_code))

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
                summoner_request = requests.get(PLATFORMS[platform]+'/lol/summoner/v4/summoners/by-name/'+player[0], headers=header)
                if summoner_request.status_code == 200:
                    summoner_body = json.loads(summoner_request.text)
                    # Get the masteries points for the player
                    masteries_request = requests.get(PLATFORMS[platform]+'/lol/champion-mastery/v4/champion-masteries/by-summoner/'+summoner_body['id'], headers=header)
                    if masteries_request.status_code == 200:
                        champs_masteries = json.loads(masteries_request.text)
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
                        db.add_player_row((player[0], summoner_body['id'], player[2], platform, mastery_row_id))
                    else:
                        print('Request for masteries for summoner {} on {} failed. Status code={}.'.format(player[0], platform, req.status_code))
                else:
                    print('Request for summoner {} on {} failed. Status code={}.'.format(player[0], platform, req.status_code))

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

