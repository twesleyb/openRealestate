def bake(cookie_dough):
    ''' Clean-up a cookies.txt file generated from Chrome extension, 
    and return a dictionary of key value pairs that is compatible with requests.
    From: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests
    '''
    cookies = {}
    with open (cookie_dough, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                if len(lineFields) == 7: 
                    cookies[lineFields[5]] = lineFields[6]
    return cookies
#EOF
