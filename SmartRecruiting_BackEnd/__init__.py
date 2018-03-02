# encoding: utf-8
# -*- coding: utf-8 -*-
"""
The flask application package.
"""

#parse arguments

from flask import Flask
from flask_cors import CORS

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testing', action='store_true') #to use the testing database
parser.add_argument('-i', '--init', action='store_true') #to use the testing database
parser.add_argument('-r', '--reinit', action='store_true') #to use the testing database
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
try:
    sys.argv.remove('-i')
except:
    pass
try:
    sys.argv.remove('--init')
except:
    pass
try:
    sys.argv.remove('-r')
except:
    pass
try:
    sys.argv.remove('--reinit')
except:
    pass


app = Flask(__name__)
app.config['TOKEN_SECRET'] = 'Secret_Token' #Change this
app.config['SECRET_KEY'] = 'Secret_Key' #Change this
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
app.config['CORS_AUTOMATIC_OPTIONS'] = True
CORS(app)

app.config['TESTING'] = args[0].testing
app.config['INIT'] = args[0].init
app.config['REINIT'] = args[0].reinit

from SmartRecruiting_BackEnd.data import DatabaseManager
dbManager = DatabaseManager()

import SmartRecruiting_BackEnd.api.routes
import SmartRecruiting_BackEnd.data
import SmartRecruiting_BackEnd.deeplearning.preprocess


