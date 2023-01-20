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

import os
ids = []
osusongsdir = os.getcwd()
files = os.listdir(osusongsdir)
def scanosudir():
    for file in files:
        sp = file.split()
        if str(sp[0]).isnumeric() == True:
            ids.append(sp[0])
    return ids
def readosrfile(FN):
    osrfile = open(FN,"r")
    ids = osrfile.read().split('\n')
    osrfile.close()
    return ids

def generateosrfile(osrfilename='songids.txt'):
    songsfile = open(osrfilename,'w')
    for idx in ids:
        songsfile.write(idx+'\n')
    songsfile.close()
def OsrRedownload(ids):
    try:
        os.mkdir("dlsongs")
    except FileExistsError:
        pass
    for map in ids:
        print(f"\nchecking {map} | {files[ids.index(map)].split(map)[1]} | item {ids.index(map)} of {len(ids)} | {int(len(ids)-int(ids.index(map)))} remaining")
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






ap = argparse.ArgumentParser(description='Osu Song Redownloader. Used in the songs directory version.')
ap.add_argument("-i", "--IDin", required=True,
                help="set it to either False to scan the songs directory, or a file name to import a file with the OSR song id structure.")
ap.add_argument("-o", "--OutFile", required=False,
                help="[filename]/False/Ignore (None); generates the songids.txt file or not.")
args = vars(ap.parse_args())
if args["IDin"] == 'False':
    ids = scanosudir()
elif not args["IDin"] == 'False':
    ids = readosrfile(args["IDin"])
if args["OutFile"] == False or args["OutFile"] == None:
    pass
else:
    generateosrfile(args["OutFile"])

OsrRedownload(ids)