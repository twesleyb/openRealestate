#!/usr/bin/env python3
''' Convert Durham realestate json file to csv.'''

import os
import json
import pandas as pd

# Path to data.
here = os.getcwd()
json_file = os.path.join(here,'data','durham-realestate.json')

# Load json as dict.
with open(json_file,'r') as json_str:
    json_dict = json.load(json_str)

# Create dataframe.
keys = json_dict.keys()
json_list = [json_dict.get(key) for key in json_dict.keys()]

# Convert to a dataframe.
df = pd.DataFrame(json_list,index=keys)

# Save as csv.
output_csv = os.path.join(here,'data','durham-realestate.csv')
df.to_csv(output_csv,index=False)
