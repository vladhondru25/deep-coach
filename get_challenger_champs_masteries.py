import requests
import json
import datetime
import time
from resources.platform import *
from resources.region import *

# Read Champions Json
with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)

# Read private key
with open('resources/MY_PRIVATE_KEY.txt') as pk_file:
    PRIVATE_KEY = pk_file.readline()

counter_requests = 0

header = {
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9,ro;q=0.8",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": PRIVATE_KEY
}
r = requests.get(PLATFORMS['eune']+'/lol/league/v4/challengerleagues/by-queue/'+'RANKED_SOLO_5x5', headers=header)
counter_requests += 1

if r.status_code == 200:
    body = json.loads(r.text)

    challenger_players = {}

    for player in body['entries']:
        # Get summoner name and its rank
        challenger_players[player['summonerName']] = player['leaguePoints']

    # Sort the players as a function of their rank in Challenger
    ordered_c_players = sorted(challenger_players.items(), key = lambda item: item[1], reverse=True)
    i=0
    for p_key,p_value in ordered_c_players:
        i += 1
        # print('Rank {}: {}'.format(i,p_key))

    champions_and_masteries = {}
    
    # Get rank 1 champion masteries
    for p_key,_ in ordered_c_players:
        response_summoner = requests.get(PLATFORMS['eune']+'/lol/summoner/v4/summoners/by-name/'+p_key, headers=header)
        counter_requests += 1
        if response_summoner.status_code == 200:
            body_summoner = json.loads(response_summoner.text)

            # Do player's champions masteries request
            champ_masteries_response = requests.get(PLATFORMS['eune']+'/lol/champion-mastery/v4/champion-masteries/by-summoner/'+body_summoner['id'], headers=header)
            counter_requests += 1
            if champ_masteries_response.status_code == 200:
                champs_masteries = json.loads(champ_masteries_response.text)
                for champ in champs_masteries:
                    last_time_played = datetime.date.today() - datetime.date.fromtimestamp(champ['lastPlayTime']/1000)

                    if last_time_played < datetime.timedelta(days=7):
                        # print( '{} played last time {}ms ago'.format(CHAMPIONS_NAMES[str(champ['championId'])], last_time_played) )
                        # print( '{} with masteries points {}'.format(CHAMPIONS_NAMES[str(champ['championId'])], champ['championPoints']) )
                        var_champ = champions_and_masteries.get(CHAMPIONS_NAMES[str(champ['championId'])],{})
                        var_champ[champ['championPoints']] = p_key
                        champions_and_masteries[CHAMPIONS_NAMES[str(champ['championId'])]] = var_champ
            else:
                print('Error champ masteries. Status code: {}'.format(champ_masteries_response.status_code))
        else:
            print('Error summoner {}. Status code: {}'.format(p_key, response_summoner.status_code))

        if counter_requests > 95:
            counter_requests = 0
            time.sleep(120)

    with open('champions_and_masteries.json', 'w') as f:
        ordered_champions_and_masteries = {k:v for k,v in sorted(champions_and_masteries.items(), key = lambda item: item[0])}

        # Order each champion masteries as a function of points
        for c_key, c_value in ordered_champions_and_masteries:
            ordered_dict = {k:v for k,v in sorted(c_value.items(), key = lambda item: int(item[0]), reverse=True)}
            ordered_champions_and_masteries[c_key] = ordered_dict

        json.dump(ordered_champions_and_masteries, f, indent=2)
    # print(champions_and_masteries)
else:
    print('Error players. Status code: {}'.format(r.status_code))