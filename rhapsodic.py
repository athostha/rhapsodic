import rhelper
import sys
import dbhelper
import os

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

def main():
    __init__()
    script = sys.argv
    num = repetition(script)
    for i in range(0,num):
        ep, serie, episodes = rhelper.sorter(rhelper.selector())
        ctime, ttime =  rhelper.player(ep, serie)
        rhelper.save(episodes, ctime, ttime, serie)

def repetition(script = 1):
    if '-c' in script:
        if len(script) > 2:
            try:num = int(script[2])
            except: num = 999
        else:
            num = 999
    else:
        num = 1
    return num


if __name__ == '__main__':
    main()
