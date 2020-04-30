def zzz(t=None,tmin=1,tmax=1.5):
    ''' Take a nap. '''
    import random
    from time import sleep
    if t is None:
        t = random.uniform(tmin,tmax)
    sleep(t)
#EOF
