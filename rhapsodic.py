import rhelper


def main():
    rhelper.__init__()
    ep, serie, episodes = rhelper.sorter(rhelper.selector())
    ctime, ttime =  rhelper.player(ep, serie)
    rhelper.save(episodes, ctime, ttime, serie)

if __name__ == '__main__':
    main()

