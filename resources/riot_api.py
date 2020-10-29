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


class Riot_API:
    def __init__(self):
        self.header = {
            # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
            # "Accept-Language": "en-US,en;q=0.9,ro;q=0.8",
            # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": PRIVATE_KEY
        }

        self.limiter_counter = 0

    def increment_limiter(self):
        self.limiter_counter += 1
    def verify_limiter(self):
        if self.limiter_counter == 95:
            time.sleep(120)
            self.limiter_counter = 0

    def get_5x5_challengers(self, platform):
        request = requests.get(PLATFORMS[platform]+'/lol/league/v4/challengerleagues/by-queue/'+'RANKED_SOLO_5x5', headers=self.header)
        if request.status_code == 200:
            return json.loads(request.text)
        else:
            print('Request for challenger players in {} failed. Status code={}.'.format(platform, request.status_code))
            return None

    def get_summoner(self, platform, summoner_name):
        request = requests.get(PLATFORMS[platform]+'/lol/summoner/v4/summoners/by-name/'+summoner_name, headers=self.header)
        if request.status_code == 200:
            return json.loads(request.text)
        else:
            print('Request for summoner {} on {} failed. Status code={}.'.format(summoner_name, platform, request.status_code))
            return None

    def get_champions_masteries(self, platform, summoner_name, summoner_id):
        request = requests.get(PLATFORMS[platform]+'/lol/champion-mastery/v4/champion-masteries/by-summoner/'+summoner_id, headers=self.header)
        if request.status_code == 200:
            return json.loads(request.text)
        else:
            print('Request for masteries for summoner {} on {} failed. Status code={}.'.format(summoner_name, platform, request.status_code))
            return None
    