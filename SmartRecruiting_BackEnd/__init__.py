"""
The flask application package.
"""

#parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testing', action='store_true') #to use the testing database
args = parser.parse_known_args()

#remove arguments to not interfere with unittest
import sys
try:
    sys.argv.remove('-t')
except:
    pass
try:
    sys.argv.remove('--testing')
except:
    pass

from flask import Flask
app = Flask(__name__)

app.config['TESTING'] = args[0].testing

import SmartRecruiting_BackEnd.api.routes
import SmartRecruiting_BackEnd.data