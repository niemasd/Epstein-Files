#! /usr/bin/env python3
'''
Upload files to the Internet Archive. I suggest initializing an Internet Archive item by uploading 1 file manually.
'''

# imports
from internetarchive import get_session
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_output
from sys import stderr
from tqdm import tqdm
import argparse

# constants
META = {
    'noarchivetorrent': 'true',
    'no-derive': 'true',
}

# upload a single file
def upload(path):
    item.upload(files=str(path), metadata=META, checksum=True, queue_derive=False, retries=100, retries_sleep=30)

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--directory', required=True, type=str, help="File Directory")
    parser.add_argument('-c', '--config', required=False, type=str, default="~/.config/internetarchive/ia.ini", help="Internet Archive CLI Config File")
    parser.add_argument('-i', '--id', required=False, type=str, default='efta_niema', help="Internet Archive Item ID")
    parser.add_argument('-t', '--threads', required=False, type=int, default=8, help="Number of Parallel Uploads")
    args = parser.parse_args()
    args.directory = Path(args.directory).expanduser()
    if not args.directory.is_dir():
        print("Directory not found: %s" % args.directory, file=stderr); exit(1)
    args.config = Path(args.config).expanduser()
    if not args.config.is_file():
        print("File not found: %s" % args.config, file=stderr); exit(1)
    if args.threads < 1:
        print("Number of threads must be positive: %d" % args.threads, file=stderr); exit(1)

    # set up Internet Archive session
    print("Initializing Internet Archive session using: %s" % args.config, file=stderr)
    session = get_session(config_file=args.config)
    print("Getting Internet Archive item: %s" % args.id, file=stderr)
    item = session.get_item(identifier=args.id)
    print("Getting existing files...")
    existing = {f.name for f in item.get_files()}
    print("Found %d existing file(s)" % len(existing), file=stderr)

    # upload new files
    print("Loading file list from: %s" % args.directory, file=stderr)
    paths = sorted(path for path in tqdm(args.directory.rglob('*.*'), unit='file') if path.name not in existing)
    print("Uploading %d new files..." % len(paths), file=stderr)
    buffer = [None] * args.threads
    buffer_ind = 0
    with tqdm(paths, unit='file') as pbar:
        for path in pbar:
            buffer[buffer_ind] = path
            buffer_ind += 1
            if buffer_ind == len(buffer):
                pbar.set_description(path.name)
                with Pool(processes=args.threads) as pool:
                    pool.map(upload, buffer)
                buffer = [None] * args.threads
            buffer_ind = 0
