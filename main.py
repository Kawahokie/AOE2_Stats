from fnmatch import fnmatchcase
from http import client
import requests
import json
import csv
import myCal
import os.path
from os import path
from tkinter import *
import random
import datetime
import time
import tkinter as tk
import threading
from queue import Queue

stats_Filename = "Stats.csv" # Init
statlist=[]
counter = 0
startDate = 1659186000
endDate = 1659189600

with open('notes.json') as json_file:
    notes_list = json.load(json_file)
urlSession = requests.Session()

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()
    
    def eventhandler(evt):  # runs in main thread
        print('Event Thread',threading.get_ident())   # event thread id (same as main)
        print(evt.state)  # 123, data from event
        string = datetime.datetime.now().strftime('%I:%M:%S %p')
        # lbl.config(text=string)  # update widget
        #txtvar.set(' '*15 + str(evt.state))  # update text entry in main thread
        
    def run(self):
        self.root=tk.Tk()
        lbl1a=tk.Label(self.root, text='Start Date:')
        lbl1b=tk.Label(self.root, text=dispStartDate)
        lbl1c=tk.Label(self.root, text=datetime.datetime.fromtimestamp(dispStartDate).strftime('%c'))
        lbl2a=tk.Label(self.root, text='End Date:')
        lbl2b=tk.Label(self.root, text=endDate)
        lbl2c=tk.Label(self.root, text=datetime.datetime.fromtimestamp(endDate).strftime('%c'))
        lbl3a=tk.Label(self.root, text='Last Received Date:')
        lbl3b=tk.Label(self.root, text=startDate)
        lbl3c=tk.Label(self.root, text=datetime.datetime.fromtimestamp(startDate).strftime('%c'))
        lbl1a.grid(row = 0, column = 0, sticky = W, pady = 2)
        lbl1b.grid(row = 0, column = 1, sticky = W, pady = 2)
        lbl1c.grid(row = 0, column = 2, sticky = W, pady = 2)
        lbl2a.grid(row = 1, column = 0, sticky = W, pady = 2)
        lbl2b.grid(row = 1, column = 1, sticky = W, pady = 2)
        lbl2c.grid(row = 1, column = 2, sticky = W, pady = 2)
        lbl3a.grid(row = 3, column = 0, sticky = W, pady = 2)
        lbl3b.grid(row = 3, column = 1, sticky = W, pady = 2)
        lbl3c.grid(row = 3, column = 2, sticky = W, pady = 2)

        lbl4a=tk.Label(self.root, text='Requests Made:')
        lbl4b=tk.Label(self.root, text=counter)
        lbl5a=tk.Label(self.root, text='Matches Received:')
        lbl5b=tk.Label(self.root, text=(counter-1)*1000)
        lbl4a.grid(row = 4, column = 0, sticky = W, pady = 2)
        lbl4b.grid(row = 4, column = 1, sticky = W, pady = 2)
        lbl5a.grid(row = 5, column = 0, sticky = W, pady = 2)
        lbl5b.grid(row = 5, column = 1, sticky = W, pady = 2)
    # def startDate(self):
    #     startDate = myCal.getMyCal(self.Tk(),0,"Choose Start Date")
    #     print(startDate)
    #     self.t3.delete(0, 'end')
    #     self.t3.insert(END, str(startDate))
    # def endDate(self):
    #     endDate = myCal.getMyCal(self.Tk(),1,"Choose End Date")
    #     self.t3.delete(0, 'end')
    #     self.t3.insert(END, str(endDate))


    # mywin=MyWindow(window)
        self.root.title('AoE2 Map Stats')
        self.root.geometry("400x300+10+10")
        # self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        # label = tk.Label(self.root, text="Hello World")
        # label.pack()
        self.root.bind("<<event1>>", self.eventhandler)
        self.root.mainloop()


def mapLookup(mapNum): # Convert map number to map name
    for x in notes_list['map_type']:
        if x['id'] == mapNum:
            return x['string']
    return 'None'

def checkMatchTime(endTime): # Have we reached the selected time
    print(statlist[-1][0]," ",datetime.datetime.fromtimestamp(statlist[-1][0]).strftime('%c'))
    if statlist[-1][0] >= endTime:
        return True
    else:
        return False


def getData(since=1658725251,count=1): # Get data from API

    # base_url2 = "/api/matches?game=aoe2de"   # Doesn't help
    # url2 = "".join([base_url,"&since=",str(since),"&count=",str(count)])
    # urlSession.mount("https://aoe2.net", ForcedIPHTTPSAdapter(dest_ip='107.178.98.244'))
    # response = urlSession.get(url2, headers={'Host': 'aoe2.net'}, verify=False)

    # base_url = "https://107.178.98.244/api/matches?game=aoe2de"
    base_url = "https://aoe2.net/api/matches?game=aoe2de"
    url = "".join([base_url,"&since=",str(since),"&count=",str(count)])

    # headers={'Host': 'aoe2.net', "User-Agent": "Chrome/81.0.4044.141"}
    # response = urlSession.get(url, headers=headers, verify=False)
    response = urlSession.get(url)
    # print(response.status_code)

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
                if player['rating'] > 950:
                    if player['civ'].isnumeric():
                        column = []
                        column.append(game['started'])
                        column.append(game['match_id'])
                        # column.append(game['name'])
                        column.append(game['version'])
                        column.append(game['num_players'])
                        column.append(mapLookup(game['map_type']))
                        # column.append(notes_list['game_type'][game['game_type']]['string'])
                        # column.append(notes_list['leaderboard'][game['leaderboard_id']]['string'])
                        column.append(notes_list['rating_type'][game['rating_type']]['string'])
                        # column.append(player['name'])
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
            # headerdata.append("name")
            headerdata.append("version")
            headerdata.append("num_players")
            headerdata.append("Map")
            # headerdata.append("leaderboard_id")
            headerdata.append("rating_type")
            # headerdata.append("player_name")
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

class MyWindow:
    def __init__(self, win):
        self.lbl1a=Label(win, text='Start Date:')
        self.lbl1b=Label(win, textvariable=dispStartDate)
        self.lbl1c=Label(win, textvariable=datetime.datetime.fromtimestamp(dispStartDate).strftime('%c'))
        self.lbl2a=Label(win, text='End Date:')
        self.lbl2b=Label(win, textvariable=endDate)
        self.lbl2c=Label(win, textvariable=datetime.datetime.fromtimestamp(endDate).strftime('%c'))
        self.lbl3a=Label(win, text='Last Received Date:')
        self.lbl3b=Label(win, textvariable=startDate)
        self.lbl3c=Label(win, textvariable=datetime.datetime.fromtimestamp(startDate).strftime('%c'))
        self.lbl1a.grid(row = 0, column = 0, sticky = W, pady = 2)
        self.lbl1b.grid(row = 0, column = 1, sticky = W, pady = 2)
        self.lbl1c.grid(row = 0, column = 2, sticky = W, pady = 2)
        self.lbl2a.grid(row = 1, column = 0, sticky = W, pady = 2)
        self.lbl2b.grid(row = 1, column = 1, sticky = W, pady = 2)
        self.lbl2c.grid(row = 1, column = 2, sticky = W, pady = 2)
        self.lbl3a.grid(row = 3, column = 0, sticky = W, pady = 2)
        self.lbl3b.grid(row = 3, column = 1, sticky = W, pady = 2)
        self.lbl3c.grid(row = 3, column = 2, sticky = W, pady = 2)

        self.lbl4a=Label(win, text='Requests Made:')
        self.lbl4b=Label(win, textvariable=counter)
        self.lbl5a=Label(win, text='Matches Received:')
        self.lbl5b=Label(win, textvariable=(counter-1)*1000)
        self.lbl4a.grid(row = 4, column = 0, sticky = W, pady = 2)
        self.lbl4b.grid(row = 4, column = 1, sticky = W, pady = 2)
        self.lbl5a.grid(row = 5, column = 0, sticky = W, pady = 2)
        self.lbl5b.grid(row = 5, column = 1, sticky = W, pady = 2)
    
# startDate = 1659186000
# endDate = 1659189600
startDate = myCal.getMyCal(0,"Choose Start Date")
endDate = myCal.getMyCal(1,"Choose End Date")
gamesPerRequest = 1000 #limit <= 1000
dispStartDate = startDate

window=Tk()
mywin=MyWindow(window)
window.title('AoE2 Map Stats')
window.geometry("400x300+10+10")
# window.update()

starttime = time.time()
lasttime = starttime
# app = App()
# def getData():
while True:
    laptime = round((time.time() - lasttime), 2)
    totaltime = round((time.time() - starttime), 2)
    print("Last Request Time: "+str(laptime))
    print("Total Time: "+str(totaltime))
    lasttime = time.time()

    counter += 1
    try:
        print(counter, "Requesting...")
        Success = True
        datafile = getData(startDate,gamesPerRequest) #Epoch Time for first game, number of requests at a time
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        Success = False
    
    if (Success):
        try:
            processData(datafile,notes_list)
            if checkMatchTime(endDate): #Set End Window for game times
                break
            else:
                startDate=(statlist[-1][0])+random.randint(1, 5)
        except:
            print("Ending due to fault.")
            break
    else:
        print("Ending due to fault.")
        break

# window.mainloop()

printHeader()
printData()
print("Done")


# Data to grab: match_id, name, version, num_players, 
# map_type, game_type, leaderboard_id, rating_type
# players:(name, rating, team, civ, won)

# Choose Date Range
# Request at starting epoch date
# check last date in epoch if less than final date then request more
