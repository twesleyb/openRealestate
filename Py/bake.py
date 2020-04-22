#!/usr/bin/en/ bash

# Clean-up cookie.txt generated from Chrome extension.
# From: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests

import re

def bake(cookie_dough):
    ''' Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests.'''
    cookie = {}
    with open (cookie_dough, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                if len(lineFields) == 7: 
                    cookie[lineFields[5]] = lineFields[6]
    return cookie
#EOF
