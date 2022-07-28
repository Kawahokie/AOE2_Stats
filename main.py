import requests
import json
import csv

response = requests.get("https://aoe2.net/api/matches?game=aoe2de&since=1658725251&count=2&leaderboard_id=4&map_type_id=16")
print(response.status_code)
#print(response.json())

# data = response.json()
# print(data)
# with open('data.json', 'w') as f:
#     json.dump(data, f)

with open('data.json') as json_file:
    datafile = json.load(json_file)

# print(datafile[0]['match_id'])
# print(datafile[0]['name'])
# print(datafile[0]['version'])
# print(datafile[0]['num_players'])
# print(datafile[0]['map_type'])
# print(datafile[0]['game_type'])
# print(datafile[0]['leaderboard_id'])
# print(datafile[0]['players'][0]['name'], datafile[0]['players'][0]['rating'], datafile[0]['players'][0]['team'], datafile[0]['players'][0]['civ'], datafile[0]['players'][0]['won'])

for game in datafile:
    for player in game['players']:
        print(game['match_id'], game['name'], game['version'], game['num_players'], game['map_type'], game['game_type'], game['leaderboard_id'], player['name'], player['rating'], player['team'], player['civ'], player['won'])

# Data to grab: match_id, name, version, num_players, 
# map_type, game_type, leaderboard_id, 
# players:(name, rating, team, civ, won)

# Opening JSON file and loading the data
# into the variable data
# jsonkeylist = json.loads(keylist)

# for key in jsonkeylist:
#     print(key)

# with open('response.csv', 'w', newline='') as csvfile:
#     fieldnames = ['name', 'city', 'Height']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     for row in data:
#         writer.writerow(row)
