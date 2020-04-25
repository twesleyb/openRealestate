def start_tor(TORRC):
    ''' Launch tor client. '''
    # Requirements:
    import subprocess
    cmd = ["tor", "-f", TORRC]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    output = process.communicate()
    return(None)
# EOF
