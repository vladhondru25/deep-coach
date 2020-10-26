import requests
import json


request = requests.get('http://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion.json')
body = json.loads(request.text)


champions_dict = {}
for champion in body['data']:
    champions_dict[body['data'][champion]['key']] = champion


# champs_json = json.dumps(champions_dict)
# with open('champions_ids.json', 'w') as f:
#     json.dump(champs_json, f)

# champs_json = json.dumps(champions_dict)
with open('champions_ids.json', 'w') as f:
    json.dump(champions_dict, f)