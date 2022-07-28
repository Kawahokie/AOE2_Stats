from fnmatch import fnmatchcase
import requests
import json
import csv
import os.path
from os import path


stats_Filename = "Stats.csv"
with open('notes.json') as json_file:
    notes_list = json.load(json_file)

response = requests.get("https://aoe2.net/api/matches?game=aoe2de&since=1658725251&count=100")
print(response.status_code)
#print(response.json())

data = response.json()
with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json') as json_file:
    datafile = json.load(json_file)

if not path.exists(stats_Filename):
    with open(stats_Filename, 'a', newline='') as f:
        writer=csv.writer(f)
        headerdata = "match_id", "name", "version", "num_players", "map_type", "game_type", "leaderboard_id", "rating_type", "player_name", "elo", "team", "civ", "won"
        writer.writerow(headerdata)

with open(stats_Filename, 'a', newline='') as f:
    writer=csv.writer(f)
    for game in datafile:
        for player in game['players']:
            if game['rating_type'] == 2 or game['rating_type'] == 4:
                statdata = game['match_id'], game['name'], game['version'], game['num_players'], notes_list['map_type'][game['map_type']-9]['string'], notes_list['game_type'][game['game_type']]['string'], notes_list['leaderboard'][game['leaderboard_id']]['string'], notes_list['rating_type'][game['rating_type']]['string'], player['name'], player['rating'], player['team'], notes_list['civ'][player['civ']-1]['string'], 1 if player['won']==True else 0
                writer.writerow(statdata)
                # statdata = game['match_id'], game['name'], game['version'], game['num_players'], game['map_type'], game['game_type'], game['leaderboard_id'], game['rating_type'], player['name'], player['rating'], player['team'], player['civ'], player['won']
                # writer.writerow(statdata)

# Data to grab: match_id, name, version, num_players, 
# map_type, game_type, leaderboard_id, rating_type
# players:(name, rating, team, civ, won)



#####
# Notes
# print(datafile[0]['match_id'])
# print(datafile[0]['name'])
# print(datafile[0]['version'])
# print(datafile[0]['num_players'])
# print(datafile[0]['map_type'])
# print(datafile[0]['game_type'])
# print(datafile[0]['leaderboard_id'])
# print(datafile[0]['players'][0]['name'], datafile[0]['players'][0]['rating'], datafile[0]['players'][0]['team'], datafile[0]['players'][0]['civ'], datafile[0]['players'][0]['won'])

# print(game['match_id'], game['name'], game['version'], game['num_players'], game['map_type'], game['game_type'], game['leaderboard_id'], player['name'], player['rating'], player['team'], player['civ'], player['won'])

# print(notes_list['civ'][0]['string'])

# def convert_val(conv_stat):
#     list(conv_stat)
#     conv_stat[10] = notes_list['civ'][conv_stat[10]-1]['string']
#     # notes_list['civ'][player['civ']-1]['string']
#     tuple(conv_stat)
#     return conv_stat