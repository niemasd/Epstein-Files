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
from pathlib import Path
from pypdf import PdfReader
from re import findall
from requests import get
from tqdm import tqdm
from sys import argv, stderr

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
        if efta_start < efta:
            url = URL_BASE + dataset_num + '/' + efta
            if '.' not in efta: # assume missing extension == PDF
                url += '.pdf'
            return url
    raise ValueError("Unable to determine document URL: %s" % efta)

# run script
if __name__ == "__main__":
    # parse user args
    if len(argv) != 4:
        print("USAGE: %s <eftas.txt> <out_dir> <cookies.json>" % argv[0], file=stderr); exit(1)
    efta_path = Path(argv[1])
    out_path = Path(argv[2])
    cookies_path = Path(argv[3])
    for path in [efta_path, cookies_path]:
        if not path.is_file():
            raise ValueError("File not found: %s" % path)
    if not out_path.is_dir():
        raise ValueError("Directory not found: %s" % out_path)

    # load EFTA list
    with open(efta_path, 'rt') as f:
        eftas = sorted({s.strip() for s in f.read().strip().split()})

    # load cookies
    with open(cookies_path, 'rt') as f:
        cookies_data = f.read().strip()
    if cookies_data.startswith('cookies'):
        cookies_data = '='.join(cookies_data.split('=')[1:]).strip()
    cookies = literal_eval(cookies_data)

    # download files and print their URLs to standard output
    done = set()
    for efta in tqdm(eftas):
        url = get_url(efta)
        curr_out_path = out_path / Path(url).name
        response = get(url, cookies=cookies)
        if curr_out_path.stem.lower().strip() == '.pdf':
            try:
                pages = PdfReader(BytesIO(response.content)).pages
                if len(pages) > 1:
                    min_ID = min(findall(PATTERN, pages[0].extract_text()))
                    max_ID = max(findall(PATTERN, pages[-1].extract_text()))
                    curr_out_path = out_path / ('%s_%s.pdf' % (min_ID, max_ID))
            except:
                raise RuntimeError("Failed to download %s from: %s" % (efta, url))
        print(url)
        with open(curr_out_path, 'wb') as f:
            f.write(response.content)
