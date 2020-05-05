def tor_session(password):
    '''
    tor_session
    '''
    # Requirements
    import sys
    from torrequest import TorRequest
    # Add HashedControlPass.
    tr=TorRequest(password=password)
    session = tr.session
    url ='https://check.torproject.org'
    response = tr.get(url)
    txt = response.text
    status = txt[txt.find('<title>') + 7 : 
            txt.find('</title>')].split('\n')[2].lstrip()
    print(status,file=sys.stderr)
    if status is "Sorry. You are not using Tor.":
        print("Continue only at your own risk.",file=sys.stderr)
    #EIF
    return(session)
# EOF

