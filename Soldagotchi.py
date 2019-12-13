# -*- coding: utf-8 -*-


import urllib
import json
import time
import os
import random
import requests
import lxml
from bs4 import BeautifulSoup, SoupStrainer

refreshdelay = 1
lasttot = 0
lastplayers = []
initialized = False
countrycache = []
seperator = "016"
countryresolver = "http://stats.jrgp.us/zabijaka1/player?name="
server_ip = "45.76.84.88"
server_port = "23075"

happy1 = "(｡◕‿‿◕｡)"
happy2 = "(/^▽^)/"
happy3 = "(๑•̀ㅂ•́)و"
sad1 = "(｡ಠ╭╮ಠ｡)"
sad2 = "(▰˘︹˘▰)"
sad3 = "(∩︵∩)"

def CheckCache(value):
    for entry in countrycache:
        if value in entry:
            return entry.split(seperator)[1]
    return "nonex"

def GetCountry(player):
  if CheckCache(player) == "nonex":
    page = requests.get(countryresolver+player)
    data = page.text
    soupinstance = BeautifulSoup(data,"lxml")
    try:
      countrycache.append(player+seperator+soupinstance.find('img').get('title'))
      return soupinstance.find('img').get('title')
    except:
      countrycache.append(player+seperator+"?")
      return "?"
  else:
    return CheckCache(player)

def GetSpace(count): 
    e = ""
    for i in range(0,count):
        e = e + " "
    return e

def MakeRequest(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

while True:
    time.sleep(refreshdelay)
    tot = 0
    os.system("clear")
    tempplayers = []
    
    players = MakeRequest("http://api.soldat.pl/v0/server/"+server_ip+"/"+server_port+"/players")
    server_info = MakeRequest("http://api.soldat.pl/v0/server/"+server_ip+"/"+server_port)
    
    for p in players["Players"]:
        tot = tot + 1
        tempplayers.append(p)
    print server_info["Name"]+" "+"["+str(tot)+"]:"
    print GetSpace(5)+"│"
    print GetSpace(5)+"│"
    print GetSpace(5)+server_info["CurrentMap"]+":"
    print GetSpace(10)+"│"
    print GetSpace(10)+"│"
    print GetSpace(10)+"Players:"
    for pl in tempplayers:
        print GetSpace(15)+pl+GetSpace(22-len(pl))+" ["+GetCountry(pl)+"]"
        
    if (initialized == False):
        lasttot = tot
        lastplayers = tempplayers
        initialized = True
    else:
        print "\n"
        if (tot > lasttot):
            diffplayers = [player for player in tempplayers if player not in lastplayers]
            print "Following player has joined the game:\n"
            for player in diffplayers:
                print "    " + player
        elif (tot < lasttot):
            diffplayers = [player for player in lastplayers if player not in tempplayers]
            print "Following player has left the game:\n"
            for player in diffplayers:
                print "    " + player
            
        if tot < server_info["MaxPlayers"]:
            if (random.randrange(1,5) == 3):
                print "A slot is avaliable, you can join! "
                print happy3
            elif (random.randrange(1,5) == 2):
                print "A slot is avaliable, you can join! "
                print happy2
            else:
                print "A slot is avaliable, you can join! "
                print happy1
        elif (random.randrange(1,5) == 3):
            print "It's full..."
            print sad3
        elif (random.randrange(1,5) == 2):
            print "It's full..."
            print sad2
        else:
            print "It's full..."
            print sad1
        lasttot = tot
        lastplayers = tempplayers
