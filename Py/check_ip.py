def check_ip():
    ''' Check what our current IP address is.
    '''
    # Requirements
    import sys
    import requests
    # Make request to get ip address.
    session = requests.Session()
    response = session.get('http://ipecho.net/plain')
    ip = response.text
    print("Current IP address: {}".format(ip),file=sys.stderr)
    return(ip)
# EOF
