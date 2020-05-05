#!/usr/bin/env python3

import re
import sys
import subprocess

# Define a function that converts report.pdf to report.text.
def convert_report(input_pdf='.temp.pdf',output_txt='.temp.txt'):
    ''' Get supplemental data associated with an address.'''
    # Convert pdf to text.
    cmd = ['pdftotext','-raw','-nopgbrk',input_pdf, output_txt]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    response = process.communicate()
    stdout, stderr = [r.decode('utf-8').strip() for r in response]
    return(stderr)
#EOF
