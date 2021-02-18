import rhelper
import sys

def main():
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
