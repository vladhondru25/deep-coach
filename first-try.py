import requests

PRIVATE_KEY = 'RGAPI-9c8e99a4-63c8-4a40-a856-3afd3f8e9561'

header = {
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9,ro;q=0.8",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": PRIVATE_KEY
}
r =requests.get('https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Legendarychamp25', headers=header)

print(r.status_code)