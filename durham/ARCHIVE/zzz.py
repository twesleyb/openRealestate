#!/usr/bin/env python3
""" A function that just sleeps for a random duration. """

import random
from time import sleep


def zzz(t=None, tmin=1, tmax=1.5):
    """ Take a nap. """
    if t is None:
        t = random.uniform(tmin, tmax)
    sleep(t)


# EOF
