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


def mapLookup(mapNum):
    for x in notes_list['map_type']:
        if x['id'] == mapNum:
            return x['string']
    return 'None'

def checkMatchTime(endTime):
    if datafile['finished'] >= endTime:
        return True
    else:
        return False

def getData(since=1658725251,count=1):
    base_url = "https://aoe2.net/api/matches?game=aoe2de"
    url = "".join([base_url,"&since=",str(since),"&count=",str(count)])
    
    response = requests.get(url)
    print(response.status_code)

    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    with open('data.json') as json_file:
        datafile = json.load(json_file)
    
    return datafile

def processData(datafile,notes_list):
    for game in datafile:
    
        for player in game['players']:
            if game['rating_type'] == 2 or game['rating_type'] == 4:
                column = []
                column.append(game['finished'])
                column.append(game['match_id'])
                column.append(game['name'])
                column.append(game['version'])
                column.append(game['num_players'])
                column.append(mapLookup(game['map_type']))
                # column.append(notes_list['map_type'][game['map_type']]['string'])
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
                # print(column)
                # writer.writerow(statdata)
    return

def printData():
    if not path.exists(stats_Filename):
        with open(stats_Filename, 'a', newline='') as f:
            writer=csv.writer(f)
            headerdata = "Match_Date", "match_id", "name", "version", "num_players", "map_type", "game_type", "leaderboard_id", "rating_type", "player_name", "elo", "team", "civ", "won"
            writer.writerow(headerdata)

    with open(stats_Filename, 'a', newline='', encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerows(statlist)
    
    return

# response = requests.get("https://aoe2.net/api/matches?game=aoe2de&since=1658725251&count=100")
datafile = getData(1658725251,1000) #Epoch Time for last game, number of requests at a time

processData(datafile,notes_list)     

printData()


# Data to grab: match_id, name, version, num_players, 
# map_type, game_type, leaderboard_id, rating_type
# players:(name, rating, team, civ, won)

# Choose Date Range
# Request at starting epoch date
# check last date in epoch if less than final date then request more
