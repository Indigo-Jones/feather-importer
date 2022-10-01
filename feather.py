import os
import sys
import argparse
import json
from pathlib import Path
from collections import ChainMap

AUTO_SEEK_ERROR_MSG = "Couldn't find GameMaker's local_settings.json file, please pass the path to the file using the -f argument"

def extract(path):
    '''extract feather settings from a file'''
    with open(path) as settings_file:
        settings = json.load(settings_file)

    return {k:v for k, v in settings.items() if k.startswith('cloud.Feather Settings.')}

def backup(*, from_, to):
    '''backup a '''
    with (open(from_) as from_file,
        open(to, 'w') as to_file):
        to_file.write(from_file.read())


def load_json(path):
    with open(path) as f:
        return json.load(f)

def dump_json(obj, path, **kwargs):
    with open(path, 'w') as f:
        json.dump(obj, f, **kwargs)

parser = argparse.ArgumentParser(description='Extract & Inject feather settings from GameMaker Studio\'s IDE settings.')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', metavar='PATH',      help='path of the file to inject', dest='inject')
group.add_argument('-e', metavar='PATH',     help='path to extract feather settings to', dest='extract')
parser.add_argument('-b', action='store_true', help='create a backup of GameMaker\'s settings', dest='backup')
parser.add_argument('-f', metavar='PATH',            help='path of GameMaker\'s local_settings.json file', dest='file')

args = parser.parse_args()


if args.file:
    local_settings = Path(args.file)
    local_settings_backup = local_settings.with_suffix('.backup')
else:
    # search the default game maker directory for a single user dir
    try:
        if sys.platform.startswith('win32'):
            gm_path = Path(os.environ['APPDATA'])/'GameMaker'
        elif sys.platform.startswith('darwin'):
            gm_path = Path.home()/'.config'/'GameMaker'
        else:
            print(AUTO_SEEK_ERROR_MSG)
            sys.exit(1)
    except KeyError:
        print(AUTO_SEEK_ERROR_MSG)
        sys.exit(1)

    if not gm_path.exists():
        print(AUTO_SEEK_ERROR_MSG)
        sys.exit(1)

    user_path = None
    for file in os.scandir(gm_path):
        if file.is_dir() and file.name != 'Cache':
            if user_path is None:
                user_path = gm_path/file
            else:
                print(AUTO_SEEK_ERROR_MSG)
                sys.exit(1)
    if user_path is None:
            print(AUTO_SEEK_ERROR_MSG)
            sys.exit(1)

    local_settings = user_path/'local_settings.json'
    local_settings_backup = user_path/'local_settings.json.backup'

if args.inject:
    if args.backup:
        backup(from_=local_settings, to=local_settings_backup)

    settings_to_inject = load_json(args.inject)
    settings = load_json(local_settings)

    # remove all old feather settings
    for k in list(settings.keys()):
        if k.startswith('cloud.Feather Settings'):
            del settings[k]
            
    # inject new feather settings
    settings.update(settings_to_inject)

    # write injected feather settings back to settings file
    dump_json(settings, local_settings, indent=4)
else:
    dump_json(extract(local_settings), args.extract, indent=4)






        

