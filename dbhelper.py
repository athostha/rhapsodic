import sqlite3
import os
import json


def __init__():
    fileexists = checkfile()
    if not fileexists:
        createdb()


def checkfile():
    try:
        dir = os.path.dirname(__file__)
        f = open(dir+"/rhapsodic.json")
        f.close()
        return True
    except IOError:
        return False

def createdb():
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json',  'w') as f:
        json.dump("[]",f)


def setserie(name, nseasons, nepisodes):
    jfile = fromfile()
    jfile.append({
        "name":name,
        "nseasons":nseasons,
        "nepisodes": nepisodes,
        "currentseason":1,
        "currentepisode":1,
        "timestamp":0,
        "finished":0,
        "watchedepisodes":0
        })
    tofile(id, jfile)


def getserie(name):
    jfile = fromfile()
    serie = list(filter(lambda serie: serie['name'] == name, jfile))
    try:
        serie[0]['id'] = jfile.index(serie[0])
    except IndexError:
        serie = []
    return serie


def getepisodenumber():
    jfile = fromfile()
    series = []
    totalepisodes = 0
    watchedepisodes = 0
    for serie in jfile:
        series.append([serie['name'],serie['nepisodes'],serie['currentepisode']])
        totalepisodes += serie['nepisodes']
        watchedepisodes += serie['currentepisode']
    return series, totalepisodes, watchedepisodes


def setnewtimestamp(id, ntt):
    jfile = fromfile()
    jfile[id]['timestamp'] = ntt
    tofile(id, jfile)


def setnewepisode(id, newepisode):
    jfile = fromfile()
    jfile[id]['currentepisode'] = newepisode
    tofile(id, jfile)
    setnewtimestamp(id, 0)


def setnewseason(id,nseason):
    jfile = fromfile()
    jfile[id]['currentseason'] = nseason
    tofile(id, jfile)


def finalizeserie(id):
    jfile = fromfile()
    jfile[id]['finished'] = 1
    tofile(id, jfile)


def tofile(id, jfile):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(jfile, fout, indent=2)


def fromfile():
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfile = json.load(fin)
    return jfile
