#!/usr/bin/env python3
''' Download report as pdf, convert it to text, and extract its key results. '''

import os
import re
import sys
import subprocess

def get_history(parcel_id): 
    #EOF

BASE_URL = 'https://property.spatialest.com/nc/durham/#/property/{}'         │
url = BASE_URL.format(address.get('Parcel ID'))

