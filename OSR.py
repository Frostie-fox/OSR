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


import os
ids = []
files = []
songformat = lambda BeatmapSetID,Artist,Title: f"{BeatmapSetID} {Artist} - {Title}"
def scandir(dir,legacy="True"):
    filesog = os.listdir(os.getcwd()+dir)
    for file in filesog:
        sp = os.listdir(os.getcwd()+f"\\{dir}\\{file}")
        sp = [s for s in sp if ".osu" in s]
        try:
            sp = os.getcwd()+f"\\{dir}\\{file}\\"+sp[0]
            with open(sp,"r", encoding='utf-8') as a:
                osufile = a.read()
        except IndexError:
                log(f"No beatmap files found for \"{file}\" | Leaving it out")
        data = {}
        datasrc = osufile.split("[Metadata]\n")[1].split("\n\n[Difficulty]")[0].split('\n')
        for _ in datasrc:
            data[_.split(":")[0]] = _.split(":")[1]
        try:
            if data['BeatmapSetID'] == "-1":
                log(f"leaving out {file}: invalid ID \"-1\"")
            else:
                ids.append(data['BeatmapSetID'])
                files.append(songformat(data['BeatmapSetID'],data['Artist'],data['Title']))
        except KeyError:
            if legacy == "True":
                log(f"ID not found in \"{data['Artist']} - {data['Title']}\"! Trying legacy mode mode")
                sp = file.split()
                if str(sp[0]).isnumeric() == True:
                    if sp[0] == "-1":
                        log(f"leaving out {file}: invalid ID \"-1\"")
                    else:
                        ids.append(sp[0])
                        files.append(file)
                else:
                    log(f"legacy mode failed! Leaving out \"{data['Artist']} - {data['Title']}\"")
            else:
                log(f"ID not found in file! Legacy mode disabled, leaving out \"{data['Artist']} - {data['Title']}\"")
    return ids,files

def readosrfile(FN):
    with open(FN,"r") as osrfile:
        files = osrfile.read().split('\n')
    for file in files:
        sp = file.split()
        log(sp[0])
        if str(sp[0]).isnumeric() == True:
            ids.append(sp[0])
    return ids,files

def generateosrfile(osrfilename='songids.txt'):
    songsfile = open(osrfilename,'w')
    for idx in files:
        if files.index(idx) == 0:
            songsfile.write(idx)
        else:
            songsfile.write('\n'+idx)
    songsfile.close()

def OsrRedownload(ids,WT,files):
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
                    break
            log(f"map done!")
        else: log(f"map Exists!");  pass
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
ap.add_argument("-L","--Legacy",required=False,help="Disable legacy mode (Fallback) by setting -l to False")
args = vars(ap.parse_args())

if args["IIT"] == 'True':
    log("Reading Osr File!",False)
    ids, files = readosrfile(args["IDin"])
else:
    log("Scanning Dir!",False)
    ids, files = scandir(args["IDin"],args['Legacy'])
if args["Legacy"] == "False": log("Legacy mode Disabled!",False)
if args["OutFile"] == False or args["OutFile"] == None:
    pass
else:
    log("making outfile!",False)
    generateosrfile(args["OutFile"])
from time import sleep
wt = args["WaitTime"]
if wt == None: wt=0
OsrRedownload(ids,int(wt),files)
logf.close()