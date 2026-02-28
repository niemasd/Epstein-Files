#! /usr/bin/env python3
'''
Make ZIP files for each dataset release
'''
from pathlib import Path
from sys import argv, stderr
from tqdm import tqdm
from zipfile import ZIP_DEFLATED, ZipFile
BOUNDS = [
    ( '1', 'EFTA00000001', 'EFTA00003158'), # https://www.justice.gov/epstein/doj-disclosures/data-set-1-files
    ( '2', 'EFTA00003159', 'EFTA00003857'), # https://www.justice.gov/epstein/doj-disclosures/data-set-2-files
    ( '3', 'EFTA00003858', 'EFTA00005704'), # https://www.justice.gov/epstein/doj-disclosures/data-set-3-files
    ( '4', 'EFTA00005705', 'EFTA00008408'), # https://www.justice.gov/epstein/doj-disclosures/data-set-4-files
    ( '5', 'EFTA00008409', 'EFTA00008528'), # https://www.justice.gov/epstein/doj-disclosures/data-set-5-files
    ( '6', 'EFTA00008529', 'EFTA00009015'), # https://www.justice.gov/epstein/doj-disclosures/data-set-6-files
    ( '7', 'EFTA00009016', 'EFTA00009675'), # https://www.justice.gov/epstein/doj-disclosures/data-set-7-files
    ( '8', 'EFTA00009676', 'EFTA00039024'), # https://www.justice.gov/epstein/doj-disclosures/data-set-8-files
    ( '9', 'EFTA00039025', 'EFTA01262781'), # https://www.justice.gov/epstein/doj-disclosures/data-set-9-files
    ('10', 'EFTA01262782', 'EFTA02212882'), # https://www.justice.gov/epstein/doj-disclosures/data-set-10-files
    ('11', 'EFTA02212883', 'EFTA02730264'), # https://www.justice.gov/epstein/doj-disclosures/data-set-11-files
    ('12', 'EFTA02730265', 'EFTA02731860'), # https://www.justice.gov/epstein/doj-disclosures/data-set-12-files
]
DATASET_NUMS = {k for k, start, end in BOUNDS}

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) not in {3,4}:
        print("USAGE: %s <efta_dir> <out_dir> [dataset_num]" % argv[0], file=stderr); exit(1)
    dir_path = Path(argv[1])
    out_path = Path(argv[2])
    for path in [dir_path, out_path]:
        if not path.is_dir():
            raise ValueError("Directory not found: %s" % path)
    if len(argv) == 4:
        dataset_num = argv[3].strip()
        if dataset_num not in DATASET_NUMS:
            raise ValueError("Invalid Data Set number: %s" % dataset_num)
    else:
        dataset_num = None

    # initialize zips
    if dataset_num is None:
        zip_paths = {k : (out_path / ('Data Set %s.zip' % k)) for k, start, end in BOUNDS + [(None,None,None)]}
    else:
        BOUNDS = [tup for tup in BOUNDS if tup[0] == dataset_num]
        zip_paths = {dataset_num : (out_path / ('Data Set %s.zip' % dataset_num))}
    for path in zip_paths.values():
        if path.exists():
            raise ValueError("Output ZIP exists: %s" % path)
    print("Initializing ZIP files in output: %s" % out_path, file=stderr)
    zips = {k : ZipFile(path, mode='w', compression=ZIP_DEFLATED, allowZip64=True, compresslevel=9) for k, path in zip_paths.items()}

    # enumerate files
    print("Enumerating files from: %s" % dir_path, file=stderr)
    paths = list(tqdm(dir_path.rglob('*.*'), unit='file'))

    # compress files
    print("Creating ZIPs...", file=stderr)
    for path in tqdm(paths, unit='file'):
        efta_upper = path.stem.split('_')[0].upper().strip()
        k = None
        for curr_k, start, end in BOUNDS:
            if start <= efta_upper <= end:
                k = curr_k; break
        if k in zips:
            zips[k].write(path, arcname=path.name)

    # close zips
    for curr_zip in zips.values():
        curr_zip.close()
