#!/usr/bin/env python3
''' Download report as pdf, convert it to text, and extract its key results. '''

import download_report
import convert_report
import parse_report

def get_report(url):
    # Download report as pdf.
    response = download_report(url,output_pdf='.temp.pdf')
    # Convert pdf report to text.
    response = convert_report(input_pdf='.temp.pdf',output_txt='.tmp.pdf')
    # Extract key-value pairs from text.
    results = parse_text(input_text='.temp.txt')
    return(results)
# EOF
