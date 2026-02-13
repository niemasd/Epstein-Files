#! /usr/bin/env python3
'''
Upload files to the Internet Archive. I suggest initializing an Internet Archive item by uploading 1 file manually.
'''
from internetarchive import get_session
from pathlib import Path
from subprocess import check_output
from sys import stderr
from tqdm import tqdm
import argparse

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--directory', required=True, type=str, help="File Directory")
    parser.add_argument('-c', '--config', required=False, type=str, default="~/.config/internetarchive/ia.ini", help="Internet Archive CLI Config File")
    parser.add_argument('-i', '--id', required=False, type=str, default='niema_efta', help="Internet Archive Item ID")
    parser.add_argument('-r', '--retries', required=False, type=int, default=100, help="Number of Retries on Failed Upload")
    parser.add_argument('-s', '--sleep', required=False, type=int, default=30, help="Amount of Time to Sleep Between Retries")
    args = parser.parse_args()
    args.directory = Path(args.directory).expanduser()
    if not args.directory.is_dir():
        print("Directory not found: %s" % args.directory, file=stderr); exit(1)
    args.config = Path(args.config).expanduser()
    if not args.config.is_file():
        print("File not found: %s" % args.config, file=stderr); exit(1)
    if args.retries < 0:
        print("Number of retries must be non-negative: %s" % args.retries, file=stderr); exit(1)
    if args.sleep < 1:
        print("Sleep time must be positive: %s" % args.sleep, file=stderr); exit(1)

    # load existing files (if user has ia CLI tool)
    print("Attempting to load existing files using 'ia list'...", file=stderr)
    try:
        existing = {l.strip() for l in check_output(['ia', 'list', args.id]).decode().strip().splitlines()}
    except:
        existing = set()
    print("Found %d existing file(s)" % len(existing), file=stderr)

    # configure Internet Archive session
    print("Initializing Internet Archive session using: %s" % args.config, file=stderr)
    session = get_session(config_file=args.config)
    print("Getting Internet Archive item: %s" % args.id, file=stderr)
    item = session.get_item(identifier=args.id)

    # upload new files
    print("Uploading files from: %s" % args.directory, file=stderr)
    for path in tqdm(args.directory.rglob('*.*')):
        if path.name not in existing:
            item.upload(files=str(path), checksum=True, queue_derive=False, verbose=True, retries=args.retries, retries_sleep=args.sleep)
