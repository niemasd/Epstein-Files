#! /usr/bin/env python3
'''
Download all EFTA files listed in a text file. To get the "cookies.json" file:

1. Open the "Network" tab of the "Developer Tools"

2. Open a single PDF on the DOJ Disclosures website (https://www.justice.gov/epstein/doj-disclosures)

3. Right click on the PDF in the Network tab, and click "Copy" -> "Copy as cURL (bash)"

4. Paste in cURL Converter: https://curlconverter.com/

5. Copy the "cookies" dictionary and save as "cookies.json"
'''

# imports
from ast import literal_eval
from io import BytesIO
from multiprocessing import Manager, Pool
from pathlib import Path
from pypdf import PdfReader
from re import findall
from requests import get
from sys import stderr
from warnings import warn
import argparse

# constants
PATTERN = 'EFTA[0-9]{8}'
URL_BASE = 'https://www.justice.gov/epstein/files/DataSet%20' # append the dataset number + / + EFTA########.pdf
FIRST_DOC = [
    ( '1', 'EFTA00000001'), # https://www.justice.gov/epstein/doj-disclosures/data-set-1-files
    ( '2', 'EFTA00003159'), # https://www.justice.gov/epstein/doj-disclosures/data-set-2-files
    ( '3', 'EFTA00003858'), # https://www.justice.gov/epstein/doj-disclosures/data-set-3-files
    ( '4', 'EFTA00005705'), # https://www.justice.gov/epstein/doj-disclosures/data-set-4-files
    ( '5', 'EFTA00008409'), # https://www.justice.gov/epstein/doj-disclosures/data-set-5-files
    ( '6', 'EFTA00008529'), # https://www.justice.gov/epstein/doj-disclosures/data-set-6-files
    ( '7', 'EFTA00009016'), # https://www.justice.gov/epstein/doj-disclosures/data-set-7-files
    ( '8', 'EFTA00009676'), # https://www.justice.gov/epstein/doj-disclosures/data-set-8-files
    ( '9', 'EFTA00039025'), # https://www.justice.gov/epstein/doj-disclosures/data-set-9-files
    ('10', 'EFTA01262782'), # https://www.justice.gov/epstein/doj-disclosures/data-set-10-files
    ('11', 'EFTA02212883'), # https://www.justice.gov/epstein/doj-disclosures/data-set-11-files
    ('12', 'EFTA02730265'), # https://www.justice.gov/epstein/doj-disclosures/data-set-12-files
]

# return the URL from an EFTA string
def get_url(efta):
    for dataset_num, efta_start in sorted(FIRST_DOC, key=lambda x: x[1], reverse=True):
        if efta_start <= efta:
            url = URL_BASE + dataset_num + '/' + efta
            if '.' not in efta: # assume missing extension == PDF
                url += '.pdf'
            return url
    raise ValueError("Unable to determine document URL: %s" % efta)

# download a given file
def download_efta(efta, DONE):
    if efta in DONE:
        return
    url = get_url(efta)
    curr_out_path = OUT_PATH / Path(url).name
    response = get(url, cookies=COOKIES)
    done = {curr_out_path.name, curr_out_path.stem}
    if curr_out_path.suffix.lower().strip() == '.pdf':
        try:
            pages = PdfReader(BytesIO(response.content)).pages
            if len(pages) > 1:
                min_ID = min(findall(PATTERN, pages[0].extract_text()))
                max_ID = max(findall(PATTERN, pages[-1].extract_text()))
                curr_out_path = OUT_PATH / ('%s_%s.pdf' % (min_ID, max_ID))
                for i in range(int(min_ID[4:]), int(max_ID[4:])+1):
                    tmp = 'EFTA' + str(i).zfill(8); done.add(tmp); done.add(tmp + '.pdf')
        except:
            warn("Failed to download %s from: %s" % (efta, url)); return None
    with open(curr_out_path, 'wb') as f:
        f.write(response.content)
    for finished_efta in done:
        DONE[finished_efta] = None
    return url

# run script
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=str, help="Input TXT with EFTA Numbers")
    parser.add_argument('-c', '--cookies', required=True, type=str, help="Input Cookies JSON")
    parser.add_argument('-o', '--output', required=True, type=str, help="Output Download Directory")
    parser.add_argument('-t', '--threads', required=False, type=int, default=8, help="Number of Threads for Downloading")
    parser.add_argument('-u', '--print_urls', action='store_true', help="Print Successful URLs to Standard Output")
    args = parser.parse_args()
    args.input = Path(args.input)
    args.cookies = Path(args.cookies)
    args.output = Path(args.output)
    for path in [args.input, args.cookies]:
        if not path.is_file():
            raise ValueError("File not found: %s" % path)
    if not args.output.is_dir():
        raise ValueError("Directory not found: %s" % args.output)
    if args.threads < 1:
        raise ValueError("Number of threads must be positive: %s" % args.threads)

    # load EFTA list
    print("Loading EFTA list from: %s" % args.input, file=stderr)
    with open(args.input, 'rt') as f:
        eftas = sorted({s.strip() for s in f.read().strip().split()})
    print("Successfully loaded %d EFTA IDs" % len(eftas), file=stderr)

    # load cookies
    print("Loading cookies from: %s" % args.cookies, file=stderr)
    with open(args.cookies, 'rt') as f:
        cookies_data = f.read().strip()
    if cookies_data.startswith('cookies'):
        cookies_data = '='.join(cookies_data.split('=')[1:]).strip()
    global COOKIES; COOKIES = literal_eval(cookies_data)

    # download files and print their URLs to standard output
    print("Downloading EFTA files...", file=stderr)
    global OUT_PATH; OUT_PATH = args.output # so each process has access to it
    with Manager() as manager:
        DONE = manager.dict()
        with Pool(processes=args.threads) as pool:
            for url in pool.starmap(download_efta, ((efta, DONE) for efta in eftas)):
                if args.print_urls and url is not None:
                    print(url)
