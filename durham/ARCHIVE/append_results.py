#!/usr/bin/env python3
""" Append a dictionary to json file. """

import json


def append_results(mydict, output_json):
    """ A function to append results to json file. """
    with open(output_json, "a") as json_file:
        json.dump(mydict, json_file)
        json_file.write("\n")
    json_file.close()


# EOF
