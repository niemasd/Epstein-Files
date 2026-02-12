#! /usr/bin/env python3
'''
Make a CSV file for an Internet Archive upload
'''
from pathlib import Path
from shutil import copy
from sys import stderr
from tqdm import tqdm
import argparse

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=str, help="Input Directory")
    parser.add_argument('-m', '--missing', required=True, type=str, help="Missing List")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output Directory")
    parser.add_argument('--dry_run', action='store_true', help="Dry Run")
    args = parser.parse_args()
    args.input = Path(args.input)
    if not args.input.is_dir():
        print("Directory not found: %s" % args.input, file=stderr); exit(1)
    args.missing = Path(args.missing)
    if not args.missing.is_file():
        print("File not found: %s" % args.missing, file=stderr); exit(1)
    args.output = Path(args.output)
    if not args.output.is_dir():
        args.output.mkdir()

    # enumerate new files (for speed)
    print("Enumerating files in: %s" % args.input, file=stderr)
    new_paths = {path.stem.split('_')[0].strip().upper():path for path in tqdm(args.input.rglob('EFTA*.*'))}
    print("Found %d files in input directory" % len(new_paths), file=stderr)

    # enumerate existing files
    print("Checking for existing files in output: %s" % args.output, file=stderr)
    existing_efta = {path.stem.split('_')[0].strip().upper() for path in tqdm(args.output.rglob('EFTA*.*'))}
    print("Found %d existing EFTA IDs" % len(existing_efta))

    # write copy to output
    print("Copying new files to output...")
    for new_efta, new_path in tqdm(new_paths.items()):
        if new_efta not in existing_efta:
            destination = args.output / new_path.name
            if args.dry_run:
                print('cp "%s" "%s"' % (new_path, destination))
            else:
                copy(new_path, destination)
