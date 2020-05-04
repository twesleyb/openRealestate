#!/usr/bin/env python3

import re
import sys

input_text = 'temp.txt'

def parse(input_text = 'temp.txt'):
    ''' Parse the text output of pdftotext. '''

# Read result from pdftotext.
with open(input_text,'r') as myfile:
    text_list = myfile.readlines()
myfile.close()

# We will collect data (values) for the following stats (keys).
keys = ['PIN','Parcel ID','Acreage','Land Use','Land Value','Land Use',
        'Deed Book', 'Deed Page', 'Plat Book', 'Plat Page', 'Subdivision',
        'Land Value', 'Building Value', 'Total Value', 'Sale Price']



def safety(fun):
    ''' '''
    def wrapper(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except AttributeError as error:
            print(error,file=sys.stderr)
            return None
    return wrapper

x = text_list[2]
get_kv_pair(x)

# works without safety. If there is a match.
#@safety
def get_kv_pair(string,key='PIN'):
    pattern = re.compile(fr"(\b{key}\b)")
    key = pattern.match(string).group(0)
    value = string.split(key)[1].strip().split(' ')[0] 
    pair = {key:value}
    return(pair)
# EOF


[ get_kv_pair(x) for x in text ]


text = [x for x in text if x != '\n'] # Drop '\n'
text = [x.strip('\n') for x in text] # Remove excess '\n'
