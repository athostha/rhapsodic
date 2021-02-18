import os
import dbhelper
import random
import subprocess
import time
import sys

def __init__():
    dir = os.path.dirname(__file__)
    path = dir + '/series/'
    dbhelper.__init__()
    series = os.listdir(path)
    for serie in series:
        spath = path + serie + '/'
        seriestats = dbhelper.getserie(serie)
        if len(seriestats) == 0:
            subs = os.listdir(spath)
            mseasons = os.path.isdir(spath + subs[0])
            if mseasons:
                nseasons = len(subs)
                nepisode = 0
                for sub in subs:
                    nepisode += len(os.listdir(spath + sub))
            else:
                nepisode = len(subs)
                nseasons = 1
            dbhelper.setserie(serie, nseasons, nepisode)

def selector():
    number, tepisodes, twatch = dbhelper.getepisodenumber()
    brute = random.randint(1, tepisodes-twatch)
    n = 0
    for num in number:
        n += num[1] - num[2]
        if n >= brute:
            selectedseries = num
            break
    return dbhelper.getserie(selectedseries[0])

def sorter(serie):
    dir = os.path.dirname(__file__)
    path = dir + '/series/' + serie[0][1] + '/'
    if serie[0][2] == 1:
        episodes = sorted(os.listdir(path))
        episode = episodes[serie[0][5]-1]
        ep = path + episode
    else:
        seasons = sorted(os.listdir(path))
        season = seasons[serie[0][4]-1]
        seasonpath = path + season + '/'
        episodes = sorted(os.listdir(seasonpath))
        episode = episodes[serie[0][5]-1]
        ep = seasonpath + episode
    return ep, serie, episodes

def player(ep,serie):
    print(serie)
    output = subprocess.run(["mpv", "-ss", str(serie[0][6]), ep],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    for i in range(1,99):
        uncodedtime = output.stdout.decode().splitlines()[-i]
        if "A-V" in uncodedtime: break
    if "(Paused)" in uncodedtime:
        uncodedtime = uncodedtime[9:]
    ut = uncodedtime[3:uncodedtime.find("(")].replace(" ", "")
    print(ut)
    currenttime = 3600*(int(ut[:2])) + 60*(int(ut[3:5])) + int(ut[6:8])
    totallength = 3600*(int(ut[9:11])) + 60*(int(ut[12:14])) + int(ut[15:17])
    return currenttime, totallength

def save(episodes, ctime, ttime, serie):
    ttime = float(ttime)
    ctime = float(ctime)
    if ctime >= ttime-20.0:
        nepisode = serie[0][5] + 1
        if nepisode <= len(episodes):
            dbhelper.setnewepisode(serie[0][0], nepisode)
        else:
#new season or finish the series
            if serie[0][2] > serie[0][4]:
                dbhelper.setnewseason(serie[0][0], serie[0][4]+1)
                dbhelper.setnewepisode(serie[0][0], 1)
            else:
                dbhelper.finalizeserie(serie[0][0])

    else:
        dbhelper.setnewtimestamp(serie[0][0], ctime)
