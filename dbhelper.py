import sqlite3


def __init__():
    fileexists = checkfile()
    if not fileexists:
        createdb()

def checkfile():
    try:
        f = open("rhapsodic.db")
        f.close()
        return True
    except IOError:
        return False

def createdb():
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE series(
    id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), nseasons int,
    nepisodes int, currentseason int, currentepisode int,
    timestamp float(4), finished int)''')
    conn.commit()
    conn.close()

def setserie(name, nseasons, nepisodes):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    s = "INSERT INTO series (name, nseasons, nepisodes, currentseason,currentepisode, timestamp, finished) VALUES ('" + name +"',"+str(nseasons)+","+str(nepisodes)+", 1, 1, 0, 0)"
    c.execute(s)
    conn.commit()
    conn.close()

def getserie(name):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    seriec = c.execute("SELECT * FROM series WHERE name='"+name+"' AND finished=0")
    serie =  list(seriec.fetchall())
    conn.close()
    return serie


def getepisodenumber():
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    series = c.execute("SELECT name, nepisodes FROM series")
    series =  list(series.fetchall())
    te = c.execute("SELECT SUM(nepisodes) FROM series")
    totalepisodes =  list(te.fetchall())[0]
    conn.close()
    return series, totalepisodes[0]





def setnewtimestamp(id, ntt):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET timestamp = "+str(ntt)+" WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)
    conn.close()

def setnewepisode(id, newepisode):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET currentepisode = "+str(newepisode)+", timestamp = 0.0 WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)


def setnewseason(id,nseason):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET currentseason = "+ str(nseason)+" WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)

def finalizeserie(id):
    conn = sqlite3.connect('rhapsodic.db')
    c = conn.cursor()
    c.execute("UPDATE series SET finished = 1 WHERE id=" + str(id))
    s = "SELECT * FROM series WHERE id = "+str(id)
    print(s)
    seriec = c.execute("SELECT * FROM series WHERE id = "+str(id))
    serie =  list(seriec.fetchall())
    print(serie)


'''conn = sqlite3.connect('rhapsodic.db')
c = conn.cursor()
seriec = c.execute("SELECT count(*) FROM series")
serie =  list(seriec.fetchall())
print(serie)
conn.close()'''

