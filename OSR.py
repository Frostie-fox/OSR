#Report - redownloaded maps
#Report - Not found on the mirrors
#Report - Good, redownloadable maps with good mode
#Report - Legacy, redownloadable with legacy mode
#Report - failed beatmaps
#Report - ammount of beatmaps
RepRED     = 0
RepNFM     = 0
RepGood    = 0
RepLeg     = 0
RepFail    = 0
RepTOT     = 0

from doctest import REPORTING_FLAGS
import requests
import argparse



from time import gmtime, strftime
with open("log.txt","w") as _:
    _.write('')
logf = open("log.txt","a")
mirrors = { 
        "beatconnect.io": "https://beatconnect.io/b/{}",
        "chimu.moe": "https://api.chimu.moe/v1/download/{}?n=1"
        }
def downL(idx,mirror,outfile="out.osz"):
    try:
        bm = requests.get(mirrors[mirror].replace("{}",idx))
        with open(outfile,"wb") as _:
            _.write(bm.content)
    except FileExistsError:
        pass
    return bm.status_code

def get(idx,mirror,outfile):
    return downL(idx,mirror,outfile)
def log(a,PE=True):
    if PE:
        print(a)
    logf.write(strftime("%d %m %Y %H:%M:%S", gmtime())+f" - {a}\n")
def sleepcus(sec):
    for _ in range(int(sec)):
        sleep(0.5)
        print(int(_)+1)
        sleep(0.5)

import os
ids = []
files = []
songformat = lambda BeatmapSetID,Artist,Title: f"{BeatmapSetID} {Artist} - {Title}"
def scandir(dir,legacy=True):
    repgood = 0
    repfail = 0
    repleg  = 0
    reptot  = 0
    filesog = os.listdir(os.getcwd()+"\\"+dir)
    for file in filesog:
        sp = os.listdir(os.getcwd()+f"\\{dir}\\{file}")
        sp = [s for s in sp if ".osu" in s]
        try:
            sp = os.getcwd()+f"\\{dir}\\{file}\\"+sp[0]
            with open(sp,"r", encoding='utf-8') as a:
                osufile = a.read()

        except IndexError:
                log(f"No beatmap files found for \"{file}\" | Leaving it out")
                repfail += 1
                reptot += 1

        data = {}
        datasrc = osufile.split("[Metadata]\n")[1].split("\n\n[Difficulty]")[0].split('\n')
        for _ in datasrc:
            data[_.split(":")[0]] = _.split(":")[1]
        try:
            if data['BeatmapSetID'] == "-1":
                log(f"leaving out {file}: invalid ID \"-1\"")
                repfail += 1
                reptot += 1
            else:
                ids.append(data['BeatmapSetID'])
                files.append(songformat(data['BeatmapSetID'],data['Artist'],data['Title']))
                repgood += 1
                reptot += 1
        except KeyError:
            if legacy:
                log(f"ID not found in \"{data['Artist']} - {data['Title']}\"! Trying legacy mode mode")
                sp = file.split()
                if str(sp[0]).isnumeric() == True:
                    if sp[0] == "-1":
                        log(f"leaving out {file}: invalid ID \"-1\"")
                        repfail += 1
                        reptot += 1
                    else:
                        ids.append(sp[0])
                        files.append(file)
                        repleg += 1
                        reptot += 1
                else:
                    log(f"legacy mode failed! Leaving out \"{data['Artist']} - {data['Title']}\"")
                    repfail += 1
                    reptot += 1
            else:
                log(f"ID not found in file! Legacy mode disabled, leaving out \"{data['Artist']} - {data['Title']}\"")
                repfail += 1
                reptot += 1
    return ids,files,len(files),[repgood,repleg,repfail,reptot]

def readosrfile(FN):
    with open(FN,"r") as osrfile:
        files = osrfile.read().split('\n')
    for file in files:
        sp = file.split()
        log(sp[0])
        if str(sp[0]).isnumeric() == True:
            ids.append(sp[0])
    return ids,files,len(files)

def generateosrfile(osrfilename='songids.txt'):
    songsfile = open(osrfilename,'w')
    for idx in files:
        if files.index(idx) == 0:
            songsfile.write(idx)
        else:
            songsfile.write('\n'+idx)
    songsfile.close()

def OsrRedownload(ids,WT,files):
    repred = 0
    try:
        os.mkdir("dlsongs")
    except FileExistsError:
        pass
    for map in ids:
        log(f"\nchecking {map} | {files[ids.index(map)].split(map)[1]} | item {ids.index(map)} of {len(ids)} | {int(len(ids)-int(ids.index(map)))} remaining")
        try:
            open(f"./dlsongs/{str(map)}.osz",'rb').close()
        except FileNotFoundError:
            for cloud in mirrors:
                log(f"downloading map with {cloud}!")
                code = get(map,cloud,f"./dlsongs/{str(map)}.osz")
                if code == 200:
                    log(f"{cloud} worked")
                    repred += 1
                    break
            log(f"map done!")
        else: log(f"map Exists!");  pass
        sleepcus(WT)
    return repred






ap = argparse.ArgumentParser(description='Osu Song Redownloader.')
ap.add_argument("-t", "--IIT", required=True,
                help="Set it to False, and give -i (or --IDin) a directory name the songs will be inside, or true, and give -i a file name for an OSR input file")
ap.add_argument("-i","--IDin", required=True,
                help="Give a directory name where the songs are, or an OSR input file")
ap.add_argument("-o", "--OutFile", required=False,
                help="[filename]/False/Ignore (None); generates the songids.txt file or not.")
ap.add_argument("-w","--WaitTime",required=False,
                help = "Wait time between beatmap downloads (in seconds)")
ap.add_argument("-L","--Legacy",required=False,help="Disable legacy mode (Fallback) by setting -l to False")
args = vars(ap.parse_args())

reps = []

if args["IIT"] == 'True':
    log("Reading Osr File!")
    ids, files,RepTOT = readosrfile(args["IDin"])
else:
    log("Scanning Dir!")
    ids, files,RepTOT,reps = scandir(args["IDin"],args['Legacy'])
if args["Legacy"] == "False": log("Legacy mode Disabled!")
if args["OutFile"] == False or args["OutFile"] == None:
    pass
else:
    log("making outfile!")
    generateosrfile(args["OutFile"])
from time import sleep
wt = args["WaitTime"]
if wt == None: wt=0
RepRED = OsrRedownload(ids,int(wt),files)


if reps != []:
    RepGood = reps[0]
    RepLeg  = reps[1]
    RepFail = reps[2]
    RepTOT  = reps[3]
    log(f"successfully redownloaded beatmaps: {round(RepRED/RepTOT)*100}%")
    log(f"beatmaps scanned with New Mode    : {round(RepGood/RepTOT)*100}%")
    log(f"beatmaps scanned with Legacy Mode : {round(RepLeg/RepTOT)*100}%")
    log(f"beatmaps that failed scanning     : {round(RepFail/RepTOT)*100}%")

logf.close()