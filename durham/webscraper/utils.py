#!/usr/bin/env python3

import random
from time import sleep
from functools import wraps


def zzz(t=None, tmin=1, tmax=1.5):
    """ A function that just sleeps for a random duration.
    Requires:
        random, time.sleep
    """
    if t is None:
        t = random.uniform(tmin, tmax)
    sleep(t)


# EOF


def combine_terms(mydict, **kwargs):
    """ Combine dictionary values into a single string. """
    vals = [mydict.get(arg) for arg in kwargs.values()]
    clean_vals = [val.strip() for val in vals]
    return " ".join(clean_vals)


# EOF


def add_method(myclass):
    """ A wrapper to add a method to an existing class.
    Requires:
        functools.wraps 
    Example:
        @add_method(A)
        def foo():
           print('hello world!')
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        setattr(myclass, func.__name__, wrapper)
        # NOTE: we are not binding func. We are binding wrapper which
        # accepts self, and does exactly the same as func.
        return func  # returning func means func can still be used normally

    return decorator


# EOF
