import requests
import json
import datetime
import time


# Read Champions Json
with open('resources/champions_ids.json') as json_file:
    CHAMPIONS_NAMES = json.load(json_file)

# Read private key
with open('MY_PRIVATE_KEY.txt') as pk_file:
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
    