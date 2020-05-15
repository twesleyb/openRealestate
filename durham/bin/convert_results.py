#!/usr/bin/env python3
''' Convert Durham realestate json file to csv.'''

import os
import json
import pandas as pd
from argparse import ArgumentParser

ap = ArgumentParser(description='Convert JSON results to csv file.')
ap.add_argument('input',type=str,help='path to realestate json file')
ap.add_argument('-o','--output',type=str,default='out.csv',help='output file')
args = vars(ap.parse_args())

# Paths to input/output.
input_json = args['input']
output_csv = args['output']

# Load json as dict.
with open(input_json,'r') as json_str:
    json_dict = json.load(json_str)

# Create dataframe.
keys = json_dict.keys()
json_list = [json_dict.get(key) for key in json_dict.keys()]

# Convert to a dataframe.
df = pd.DataFrame(json_list,index=keys)

# Save as csv.
df.to_csv(output_csv,index=False)
