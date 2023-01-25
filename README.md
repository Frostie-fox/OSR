# OSR
Osu Song Redownloader

# info
To use it, at least two arguments needs to be given:

	File or Directory (Id In Type): -t, True or False (False = Directory)

	Directory / File Name (Id in): -i the name of the file/directory for the song ids
There are optional arguments:

	Outfile: -o, either False (can ignore too) or any value, which will be the file name.

	Wait: -w, which will wait a specific time ammount before downloading the next beatmap (in seconds)
There are planned to be two modes:
	Legacy/Classic: reads the info from the title

	New: reads beatmap metadata from a(n) .osu file



# Run like this:
```
py -m OSR.py --help
```
# File Modes:
Legacy: Reads the info from folder title

New Mode: Reads info from beatmap .osu file "[metadata]" section

If New Mode fails, legacy mode will execute by default, which can be disabled with "-L False"

# disclaimer:
	I am in no way shape or form affiliated with OSU and their developers. I am a person alone, with too much free time, who decided to automate a simple but time consuming task.
	If any Copyright issues pop up, they are completely unintentional, and i am willing to remove any conflicting content.
	I am not responsible for any damages done by any user using this tool, as i do not encourage people to use this tool in a bad way.
	This project does not do anything with Osu replay files (*.OSR files)