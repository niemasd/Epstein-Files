#!/usr/bin/env bash
# Use pdftotext and grep to extract all EFTA######## numbers from a PDF
if [ "$#" -ne 1 ] ; then
    echo "USAGE: $0 <PDF>"; exit 1
fi
pdftotext "$1" - | grep -E 'EFTA[0-9]{8}' | sort | uniq
