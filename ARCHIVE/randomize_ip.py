def randomize_ip(password,quiet=False):
    ''' Randomize IP addredss with tor.
    Reset tor to randomize your IP address. Takes your tor hashed control
    password as an argument. Requires that you have set HashedControlPassword 
    variable in the tor configuration file.
    '''
    # Requirements
    import sys
    from torrequest import TorRequest
    # Add HashedControlPass.
    tr=TorRequest(password=password)
    # Reset Tor.
    tr.reset_identity()
    # Check new ip.
    response = tr.get('http://ipecho.net/plain')
    ip = response.text
    if not quiet:
        print("IP address is set to: {}".format(ip),file=sys.stderr)
    return(ip)
# EOF
