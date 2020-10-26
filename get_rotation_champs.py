import requests
import json

EUNE_URL = 'https://eun1.api.riotgames.com'

# Read Json
with open('champions_ids.json') as json_file:
    champs_names = json.load(json_file)

# Read private key
with open('MY_PRIVATE_KEY.txt') as pk_file:
    PRIVATE_KEY = pk_file.readline()

header = {
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9,ro;q=0.8",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": PRIVATE_KEY
}
r = requests.get(EUNE_URL+'/lol/platform/v3/champion-rotations', headers=header)

if r.status_code == 200:
    body = json.loads(r.text)

    free_champ_list = []
    for free_champ in body['freeChampionIds']:
        free_champ_list.append(champs_names[str(free_champ)])

    free_champ_list.sort()

    for free_champ in free_champ_list:
        print(free_champ)
