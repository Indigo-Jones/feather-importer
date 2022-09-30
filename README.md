# feather-importer
Import and export feather settings for the GameMaker IDE

## Guide

This tool is intended to allow you import and extract feather settings from the GameMaker IDE.
First, if you have feather settings you want to save, extract them from the IDE using the command `py feather.py -e old_settings.json`.
The program will automatically look for the game maker settings file, if it can't find it (because the game maker install has been moved
from the default location, or there are multiple accounts associated with a single GameMaker install) this will fail and you must specify
the file location of the settings file using the -f argument,

Next, take a json file containing the feather settings you want to import and use the command `py feather.py -i new_settings.json` to import
the new settings into the IDE. This will overwrite *all* feather settings in the IDE, even ones not specified in the imported settings file.
Optionally you can use the -b flag to make a backup of the settings you are overwriting in case anything goes wrong, this backup will be located
in the same directory as local_settings.json and will be called local_settings.json.backup.


## Usage:
```
usage: feather.py [-h] (-i PATH | -e PATH) [-b] [-f PATH]

Extract & Inject feather settings from GameMaker Studio's IDE settings.

options:
  -h, --help  show this help message and exit
  -i PATH     path of the file to inject
  -e PATH     path to extract feather settings to
  -b          create a backup of GameMaker's settings
  -f PATH     path of GameMaker's local_settings.json file
```
## Examples:

extract all feather settings to a file called `settings.json`
```
py feather.py -e settings.json
```

inject the feather settings in `settings.json` into the gamemaker IDE 
```
py feather.py -i settings.json
```

inject the feather settings in `settings.json` into the file specified by the `-f` argument
```
py feather.py -i settings.json -b -f "C:\Users\User\AppData\Roaming\GameMakerStudio2\gamemakerusername\local_settings.json"
```
