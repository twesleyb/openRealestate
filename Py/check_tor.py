def check_tor(password):
    ''' Check if we are connected via tor.
    '''
    # Requirements
    import sys
    from torrequest import TorRequest
    # Add HashedControlPass.
    tr=TorRequest(password=password)
    # Check that we are connected via tor.
    url ='https://check.torproject.org'
    response = tr.get(url)
    txt = response.text
    status = txt[txt.find('<title>') + 7 : 
            txt.find('</title>')].split('\n')[2].lstrip()
    print(status,file=sys.stderr)
# EOF

