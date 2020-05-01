"""
1. Read creds file, extract username, pass
2. format as proper string to pass back to shell script
    "{username}:{password}" for curl command
3. in shell script, AUTH=`python get_creds.py`, then curl $AUTH to start session

Or, just use python to start a session or something.
"""

import json
import sys

creds_file = sys.argv[1]
with open(creds_file, 'r') as f:
    creds = json.load(f)

return_str = ':'.join([creds['username'], creds['password']])
print(return_str)
