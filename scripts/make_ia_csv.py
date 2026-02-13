#! /usr/bin/env python3
'''
Make a CSV file for an Internet Archive upload. Use with: ia upload --spreadsheet=upload.csv --metadata="no-derive:true" --no-derive
'''
from gzip import open as gopen
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
    parser.add_argument('-mi', '--meta_id', required=False, type=str, default='niema_efta', help="Metadata: Internet Archive ID")
    parser.add_argument('-mc', '--meta_creator', required=False, type=str, default='U.S. Department of Justice', help="Metadata: Creator")
    parser.add_argument('-ml', '--meta_language', required=False, type=str, default='English', help="Metadata: Language")
    parser.add_argument('-mt', '--meta_type', required=False, type=str, default='texts', help="Metadata: Media Type")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File (CSV)")
    args = parser.parse_args()
    args.directory = Path(args.directory)
    if not args.directory.is_dir():
        print("Directory not found: %s" % args.directory, file=stderr); exit(1)
    if args.output == 'stdout':
        from sys import stdout as out_f
    else:
        args.output = Path(args.output)
        if args.output.exists():
            print("Output file exists: %s" % args.output, file=stderr); exit(1)
        elif args.output.suffix.lower() == '.gz':
            out_f = gopen(args.output, 'wt')
        else:
            out_f = open(args.output, 'wt')

    # load existing files (if user has ia CLI tool)
    print("Attempting to load existing files using 'ia list'...", file=stderr)
    try:
        existing = {l.strip() for l in check_output(['ia', 'list', args.meta_id]).decode().strip().splitlines()}
    except:
        existing = set()
    print("Found %d existing file(s)" % len(existing), file=stderr)

    # enumerate files (for speed)
    print("Enumerating files in: %s" % args.directory, file=stderr)
    paths = sorted(path for path in tqdm(args.directory.rglob('*.*')) if path.name not in existing)
    print("Found %d files" % len(paths), file=stderr)

    # write CSV output
    print("Writing output CSV: %s" % args.output, file=stderr)
    out_f.write("identifier,file,creator,language,mediatype\n")
    for path in tqdm(paths):
        out_f.write(args.meta_id) # identifier
        out_f.write(',')
        out_f.write(str(path.resolve())) # file
        out_f.write(',')
        out_f.write(args.meta_creator) # creator
        out_f.write(',')
        out_f.write(args.meta_language) # language
        out_f.write(',')
        out_f.write(args.meta_type) # mediatype
        out_f.write('\n')
    out_f.close()
