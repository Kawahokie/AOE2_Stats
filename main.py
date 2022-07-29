from fnmatch import fnmatchcase
import requests
import json
import csv
import os.path
from os import path


stats_Filename = "Stats.csv"
statlist=[]
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

for game in datafile:
    column = []
    for player in game['players']:
        if game['rating_type'] == 2 or game['rating_type'] == 4:
            column.append(game['match_id'])
            column.append(game['name'])
            column.append(game['version'])
            column.append(game['num_players'])
            column.append(game['map_type'])
            # column.append(notes_list['map_type'][game['map_type']-9]['string'])
            column.append(notes_list['game_type'][game['game_type']]['string'])
            column.append(notes_list['leaderboard'][game['leaderboard_id']]['string'])
            column.append(notes_list['rating_type'][game['rating_type']]['string'])
            column.append(player['name'])
            column.append(player['rating'])
            column.append(player['team'])
            column.append(notes_list['civ'][player['civ']-1]['string'])
            column.append(1 if player['won']==True else 0)
            statlist.append(column)
            # statdata = game['match_id'], game['name'], game['version'], game['num_players'], notes_list['map_type'][game['map_type']-9]['string'], notes_list['game_type'][game['game_type']]['string'], notes_list['leaderboard'][game['leaderboard_id']]['string'], notes_list['rating_type'][game['rating_type']]['string'], player['name'], player['rating'], player['team'], notes_list['civ'][player['civ']-1]['string'], 1 if player['won']==True else 0
            print(column)
            # writer.writerow(statdata)
            

if not path.exists(stats_Filename):
    with open(stats_Filename, 'a', newline='') as f:
        writer=csv.writer(f)
        headerdata = "match_id", "name", "version", "num_players", "map_type", "game_type", "leaderboard_id", "rating_type", "player_name", "elo", "team", "civ", "won"
        writer.writerow(headerdata)

with open(stats_Filename, 'a', newline='', encoding='utf-8-sig') as f:
    writer=csv.writer(f)
    writer.writerows(statlist)


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