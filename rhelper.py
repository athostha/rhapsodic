import os
import dbhelper
import random
import subprocess
import time
import sys
import re


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
    path = dir + '/series/' + serie[0]['name'] + '/'
    if serie[0]['nseasons'] == 1:
        episodes = sorted(os.listdir(path))
        episode = episodes[serie[0]["currentepisode"]-1]
        ep = path + episode
    else:
        seasons = sorted(os.listdir(path))
        season = seasons[serie[0]["currentseason"]-1]
        seasonpath = path + season + '/'
        episodes = sorted(os.listdir(seasonpath))
        episode = episodes[serie[0]["currentepisode"]-1]
        ep = seasonpath + episode
    return ep, serie, episodes

def player(ep,serie):
    print(str(serie[0]['id']) , serie[0]['name'])
    print('S{:02d}E{:02d}'.format(serie[0]['currentseason'], serie[0]['currentepisode']))
    output = subprocess.run(["mpv", "-ss", str(serie[0]['timestamp']), ep],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    for i in range(1,99):
        uncodedtime = output.stdout.decode().splitlines()[-i]
        if "A-V" in uncodedtime: break
    if "(Paused)" in uncodedtime:
        uncodedtime = uncodedtime[9:]
    ut = re.findall(r'[0-1]{0,1}[0-9]{1,2}:[0-5][0-9]:[0-5][0-9]', uncodedtime)
    print(ut)
    currenttime = 3600*(int(ut[0][:2])) + 60*(int(ut[0][3:5])) + int(ut[0][6:8])
    totallength = 3600*(int(ut[1][:2])) + 60*(int(ut[1][3:5])) + int(ut[1][6:8])
    return currenttime, totallength

def save(episodes, ctime, ttime, serie):
    ttime = float(ttime)
    ctime = float(ctime)
    if ctime >= ttime-20.0:
        nepisode = serie[0]["currentepisode"] + 1
        if nepisode <= len(episodes):
            dbhelper.setnewepisode(serie[0]['id'], nepisode)
        else:
#new season or finish the series
            if serie[0][2] > serie[0][4]:
                dbhelper.setnewseason(serie[0]['id'], serie[0][4]+1)
                dbhelper.setnewepisode(serie[0]['id'], 1)
            else:
                dbhelper.finalizeserie(serie[0]['id'])

    else:
        dbhelper.setnewtimestamp(serie[0]['id'], ctime)

def listing():
    listing = dbhelper.fromfile()
    counter = 0
    for serie in listing:
        print("{:03d} |{:^40} | S{:02d}E{:02d}".format(counter, serie['name'],serie['currentseason'], serie['currentepisode']))
        counter +=1

def this(id):
    serie = dbhelper.fromfile()
    serie[id]['id'] = id
    return sorter([serie[id]])
