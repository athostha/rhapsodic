import sqlite3
import os


def __init__():
    fileexists = checkfile()
    if not fileexists:
        createdb()

def checkfile():
    try:
        dir = os.path.dirname(__file__)
        f = open(dir+"/rhapsodic.db")
        f.close()
        return True
    except IOError:
        return False

def createdb():
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE series(
    id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), nseasons int,
    nepisodes int, currentseason int, currentepisode int,
    timestamp float(4), finished int, watchedepisodes int)''')
    conn.commit()
    conn.close()
def setserie(name, nseasons, nepisodes):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    s = "INSERT INTO series (name, nseasons, nepisodes, currentseason,currentepisode, timestamp, finished, watchedepisodes) VALUES ('" + name +"',"+str(nseasons)+","+str(nepisodes)+", 1, 1, 0, 0, 0)"
    c.execute(s)
    conn.commit()
    conn.close()

def getserie(name):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    chamado = "SELECT * FROM series WHERE name='"+name+"' AND finished=0"
    serie1 = c.execute(chamado)
    serie =  list(serie1.fetchall())
    conn.close()
    return serie


def getepisodenumber():
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    series = c.execute("SELECT name, nepisodes, watchedepisodes FROM series")
    series =  list(series.fetchall())
    te = c.execute("SELECT SUM(nepisodes) FROM series")
    totalepisodes =  list(te.fetchall())[0]
    tw = c.execute("SELECT SUM(watchedepisodes) FROM series")
    watchedepisodes =  list(tw.fetchall())[0]
    conn.close()
    return series, totalepisodes[0], watchedepisodes[0]





def setnewtimestamp(id, ntt):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET timestamp = "+str(ntt)+" WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)
    conn.commit()
    conn.close()

def setnewepisode(id, newepisode):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET currentepisode = "+str(newepisode)+", timestamp = 0.0, watchedepisodes = watchedepisodes + 1 WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)
    conn.commit()
    conn.close()


def setnewseason(id,nseason):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET currentseason = currentseason + 1, watchedepisodes = watchedepisodes + 1 WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)
    conn.commit()
    conn.close()

def finalizeserie(id):
    dir = os.path.dirname(__file__)
    conn = sqlite3.connect(dir+'/rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET finished = 1 WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)
    conn.commit()
    conn.close()


'''conn = sqlite3.connect('rhapsodic.db')
c = conn.cursor()
seriec = c.execute("SELECT count(*) FROM series")
serie =  list(seriec.fetchall())
print(serie)
conn.close()'''

