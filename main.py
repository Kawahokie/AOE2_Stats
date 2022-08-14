from fnmatch import fnmatchcase
from http import client
import requests
import json
import csv
import myCal
import os.path
from os import path
from tkinter import *


import time
# import pycurl # Not used
# from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter  # Not used

# from tkcalendar import Calendar, DateEntry

# import logging
# import http.client
# http.client.HTTPConnection.debuglevel =1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

stats_Filename = "Stats.csv" # Init
statlist=[]
counter = 0
startDate = 1659186000
endDate = 1659189600
with open('notes.json') as json_file:
    notes_list = json.load(json_file)
urlSession = requests.Session()

def mapLookup(mapNum): # Convert map number to map name
    for x in notes_list['map_type']:
        if x['id'] == mapNum:
            return x['string']
    return 'None'

def checkMatchTime(endTime): # Have we reached the selected time
    print(statlist[-1][0])
    if statlist[-1][0] >= endTime:
        return True
    else:
        return False

# def useCurl(since=1658725251,count=1):
#     base_url = "https://aoe2.net/api/matches?game=aoe2de"
#     url = "".join([base_url,"&since=",str(since),"&count=",str(count)])
#     with open('out.html', 'wb') as f:
#         c = pycurl.Curl()
#         c.setopt(c.URL, url)
#         c.setopt(c.WRITEDATA, f)
#     try:
#         c.perform()
#         c.close()
#     except pycurl.error as exc:
#         return "Unable to reach %s (%s)" % (url, exc)


def getData(since=1658725251,count=1): # Get data from API

    # base_url2 = "/api/matches?game=aoe2de"   # Doesn't help
    # url2 = "".join([base_url,"&since=",str(since),"&count=",str(count)])
    # urlSession.mount("https://aoe2.net", ForcedIPHTTPSAdapter(dest_ip='107.178.98.244'))
    # response = urlSession.get(url2, headers={'Host': 'aoe2.net'}, verify=False)

    base_url = "https://107.178.98.244/api/matches?game=aoe2de"
    # base_url = "https://aoe2.net/api/matches?game=aoe2de"
    url = "".join([base_url,"&since=",str(since),"&count=",str(count)])

    # response = requests.get(url)
    # headers = {"User-Agent": "Chrome/81.0.4044.141"}
    headers={'Host': 'aoe2.net', "User-Agent": "Chrome/81.0.4044.141"}
    response = urlSession.get(url, headers=headers, verify=False)
    print(response.status_code)

    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    with open('data.json') as json_file:
        datafile = json.load(json_file)
    
    return datafile

def processData(datafile,notes_list): # Load stats file
    for game in datafile:
    
        for player in game['players']:
            if game['rating_type'] == 2 or game['rating_type'] == 4:
                column = []
                column.append(game['started'])
                column.append(game['match_id'])
                column.append(game['name'])
                column.append(game['version'])
                column.append(game['num_players'])
                column.append(mapLookup(game['map_type']))
                # column.append(notes_list['game_type'][game['game_type']]['string'])
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

def printHeader():
    if not path.exists(stats_Filename): # Load Header and Print to csv
        with open(stats_Filename, 'a', newline='') as f:
            writer=csv.writer(f)
            headerdata = []
            headerdata.append("Match_Date")
            headerdata.append("match_id")
            headerdata.append("name")
            headerdata.append("version")
            headerdata.append("num_players")
            headerdata.append("Map")
            headerdata.append("leaderboard_id")
            headerdata.append("rating_type")
            headerdata.append("player_name")
            headerdata.append("elo")
            headerdata.append("team")
            headerdata.append("civ")
            headerdata.append("won")
            writer.writerow(headerdata)
    return

def printData():
    # Print Data
    with open(stats_Filename, 'a', newline='', encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerows(statlist)
    
    return

# response = requests.get("https://aoe2.net/api/matches?game=aoe2de&since=1658725251&count=100")

# class MyWindow:
#     def __init__(self, win):
#         self.lbl1=Label(win, text='First number')
#         self.lbl2=Label(win, text='Second number')
#         self.lbl3=Label(win, text='Result')
#         self.t1=Entry(bd=3)
#         self.t2=Entry()
#         self.t3=Entry()
#         self.btn1 = Button(win, text='Choose Start Date')
#         self.btn2=Button(win, text='Choose End Date')
#         self.lbl1.place(x=100, y=50)
#         self.t1.place(x=200, y=50)
#         self.lbl2.place(x=100, y=100)
#         self.t2.place(x=200, y=100)
#         self.b1=Button(win, text='Choose Start Date', command=self.startDate)
#         self.b2=Button(win, text='Choose End Date', command=self.endDate)
#         self.b1.place(x=100, y=150)
#         self.b2.place(x=250, y=150)
#         self.lbl3.place(x=100, y=200)
#         self.t3.place(x=200, y=200)
#     def startDate(self):
#         startDate = myCal.getMyCal(self.Tk(),0,"Choose Start Date")
#         print(startDate)
#         self.t3.delete(0, 'end')
#         self.t3.insert(END, str(startDate))
#     def endDate(self):
#         endDate = myCal.getMyCal(self.Tk(),1,"Choose End Date")
#         self.t3.delete(0, 'end')
#         self.t3.insert(END, str(endDate))

# window=Tk()
# mywin=MyWindow(window)
# window.title('Hello Python')
# window.geometry("400x300+10+10")
# window.mainloop()


## btn = Button(window, text='OK')
## btn.bind('<Button-1>', MyButtonClicked)
## btn = Button(window, text='OK', command=myCal.getMyCal(0,"Choose Start Date"))
## btn.pack(pady=10)
## Btn = Button(window,text="title_Text",padx=10,pady=10,command=myCal.getMyCal(0,"Choose Start Date"))
## btn.place(x=80, y=100)

# startDate = 1659186000
# endDate = 1659189600
startDate = myCal.getMyCal(0,"Choose Start Date")
endDate = myCal.getMyCal(1,"Choose End Date")
gamesPerRequest = 1000 #limit <= 1000

# root = tk.Tk()
# s = ttk.Style(root)
# s.theme_use('clam')

# ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
# ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)
# root.mainloop()

while True:
    counter += 1
    # useCurl() # Doesn't help
    # print(counter)

    try:
        print(counter)
        Success = True
        datafile = getData(startDate,gamesPerRequest) #Epoch Time for first game, number of requests at a time
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        Success = False
    
    if (Success):
        processData(datafile,notes_list)
        if checkMatchTime(endDate): #Set End Window for game times
            break
        else:
            startDate=statlist[-1][0]+1
    else:
        print("Ending due to fault.")
        break

printHeader()
printData()
print("Done")


# Data to grab: match_id, name, version, num_players, 
# map_type, game_type, leaderboard_id, rating_type
# players:(name, rating, team, civ, won)

# Choose Date Range
# Request at starting epoch date
# check last date in epoch if less than final date then request more
