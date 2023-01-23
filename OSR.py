import requests
import argparse
mirrors = { 
        "beatconnect.io": "https://beatconnect.io/b/{}",
        "chimu.moe": "https://api.chimu.moe/v1/download/{}?n=1"
        }
def downL(link,outfile="out.osz"):
    try:
        bm = requests.get(link)
        _ = open(outfile,"wb")
        _.write(bm.content)
        _.close()
    except FileExistsError:
        pass
    return bm.status_code

def get(idx,mirror,outfile):
    return downL(mirrors[mirror].replace("{}",idx),outfile)

def osrprint(ID,DATA,CURR,TOT,REM,DISDAT): #not an intentional re:zero reference.
    #print(f"\nchecking {map} | {files[ids.index(map)].split(map)[1]} | item {ids.index(map)} of {len(ids)} | {int(len(ids)-int(ids.index(map)))} remaining")
    if DISDAT == True:
        print(f"\nchecking {ID} | item {CURR} of {TOT} | {REM} remaining")
    else:
        print(f"\nchecking {ID} | {DATA} | item {CURR} of {TOT} | {REM} remaining")

import os
ids = []
files = []
def scandir(dir):
    files = os.listdir(os.getcwd()+dir)
    for file in files:
        sp = file.split()
        if str(sp[0]).isnumeric() == True:
            ids.append(sp[0])
    return ids,files
def readosrfile(FN):
    osrfile = open(FN,"r")
    files = osrfile.read().split('\n')
    osrfile.close()
    for file in files:
        sp = file.split()
        if str(sp[0]).isnumeric() == True:
            ids.append(sp[0])
    return ids,files

def generateosrfile(osrfilename='songids.txt'):
    songsfile = open(osrfilename,'w')
    for idx in files:
        if files.index(idx) is 0:
            songsfile.write(idx)
        else:
            songsfile.write('\n'+idx)
    songsfile.close()
def OsrRedownload(ids,WT,files,disablefiles=False):
    try:
        os.mkdir("dlsongs")
    except FileExistsError:
        pass
    for map in ids:
        #osrprint(ID,DATA,CURR,TOT,REM)
        if disablefiles is not True:
            osrprint(map,files[ids.index(map)].split(map)[1],ids.index(map),len(ids),int(len(ids)-int(ids.index(map))),False)
        else:
            osrprint(map,'',ids.index(map),len(ids),int(len(ids)-int(ids.index(map))),True)
        #print(f"\nchecking {map} | {files[ids.index(map)].split(map)[1]} | item {ids.index(map)} of {len(ids)} | {int(len(ids)-int(ids.index(map)))} remaining")
        try:
            open(f"./dlsongs/{str(map)}.osz",'rb').close()
        except FileNotFoundError:
            for cloud in mirrors:
                print(f"downloading map!")
                code = get(map,cloud,f"./dlsongs/{str(map)}.osz")
                if code == 200:
                    print(f"{cloud} worked")
                    break
                print(f"map done!")
        else: print(f"map Exists!");  pass
        sleep(WT)






ap = argparse.ArgumentParser(description='Osu Song Redownloader.')
ap.add_argument("-t", "--IIT", required=True,
                help="Set it to False, and give -i (or --IDin) a directory name the songs will be inside, or true, and give -i a file name for an OSR input file")
ap.add_argument("-i","--IDin", required=True,
                help="Give a directory name where the songs are, or an OSR input file")
ap.add_argument("-o", "--OutFile", required=False,
                help="[filename]/False/Ignore (None); generates the songids.txt file or not.")
ap.add_argument("-w","--WaitTime",required=False,
                help = "Wait time between beatmap downloads (in seconds)")
args = vars(ap.parse_args())
fileEnable = False

if args["IIT"] == 'True':
    ids, files = readosrfile(args["IDin"])
    filesEnable = True
else:
    ids, files = scandir(args["IDin"])
    filesEnable=True
    
if args["OutFile"] == False or args["OutFile"] == None:
    pass
else:
    generateosrfile(args["OutFile"])
from time import sleep
wt = args["WaitTime"]
if wt == None: wt=0
OsrRedownload(ids,int(wt),files,False)