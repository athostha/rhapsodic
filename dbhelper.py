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
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfin = json.load(fin)
        jfile = json.loads(jfin)
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
    fjson = json.dumps(jfile)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(fjson, fout)

def getserie(name):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfile = json.load(fin)
        jlist  = json.loads(jfile)
        serie = list(filter(lambda serie: serie['name'] == name, jlist))
        try:
            serie[0]['id'] = jlist.index(serie[0])
        except IndexError:
            serie = []
    return serie


def getepisodenumber():
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfile = json.load(fin)
        jlist  = json.loads(jfile)
    series = []
    totalepisodes = 0
    watchedepisodes = 0
    for serie in jlist:
        series.append([serie['name'],serie['nepisodes'],serie['currentepisode']])
        totalepisodes += serie['nepisodes']
        watchedepisodes += serie['currentepisode']
    return series, totalepisodes, watchedepisodes





def setnewtimestamp(id, ntt):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfin = json.load(fin)
        jfile = json.loads(jfin)
    jfile[id]['timestamp'] = ntt
    fjson = json.dumps(jfile)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(fjson, fout)


def setnewepisode(id, newepisode):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfin = json.load(fin)
        jfile = json.loads(jfin)
    jfile[id]['currentepisode'] = newepisode
    fjson = json.dumps(jfile)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(fjson, fout)

def setnewseason(id,nseason):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfin = json.load(fin)
        jfile = json.loads(jfin)
    jfile[id]['currentseason'] = nseason
    fjson = json.dumps(jfile)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(fjson, fout)

def finalizeserie(id):
    dir = os.path.dirname(__file__)
    with open(dir+'/rhapsodic.json') as fin:
        jfin = json.load(fin)
        jfile = json.loads(jfin)
    jfile[id]['finished'] = 1
    fjson = json.dumps(jfile)
    with open(dir+'/rhapsodic.json', 'w') as fout:
        json.dump(fjson, fout)
