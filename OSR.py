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
osusongsdir = os.getcwd() + "\\Songs"
files = os.listdir(osusongsdir)
ids = []

for file in files:
    sp = file.split()
    if str(sp[0]).isnumeric() == True:
        ids.append(sp[0])


songsfile = open('songids.txt','w')
for idx in ids:
    songsfile.write(idx+'\n')
songsfile.close()
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






ap = argparse.ArgumentParser(description='Osu Song Redownloader')
ap.add_argument("-f", "--file", required=False,
                help="a text file containing beatmap ids seperated by newline")