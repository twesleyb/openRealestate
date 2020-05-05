#!/usr/bin/env python3

import sys
from os import getcwd, listdir
from os.path import isdir, join, dirname

def getrd(here=getcwd(),dpattern=".git",max_tries=5):
    ''' Find a git repositories root directory.'''
    # Initial params
    tries = 0
    root = False
    here = getcwd()
    # While loop to try and find project root.
    while not root and tries < max_tries:
        onlydirs = [d for d in listdir(here) if isdir(join(here, d))]
        root = dpattern in onlydirs
        if not root: 
            here = dirname(here)
            tries += 1
    # Return root directory.
    root_dir = here
    return(root_dir)
# EOF

if __name__ == '__main__':
    print(getrd(),file=sys.stdout)
