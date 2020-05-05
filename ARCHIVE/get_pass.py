def get_pass(key):
    ''' Get password from password store. '''
    # Requirements:
    import re
    import subprocess
    cmd = ["pass",key]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    output = process.communicate()

    password = re.split(" |\n",list(output)[0].decode('utf-8'))[1]
    return(password)
# EOF
