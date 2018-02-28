"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS
from SmartRecruiting_BackEnd.data import DatabaseManager

dbManager = DatabaseManager()

app = Flask(__name__)
app.config['TOKEN_SECRET'] = 'Secret_Token' #Change this
app.config['SECRET_KEY'] = 'Secret_Key' #Change this
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
app.config['CORS_AUTOMATIC_OPTIONS'] = True
CORS(app)

import SmartRecruiting_BackEnd.api.routes
import SmartRecruiting_BackEnd.data
import SmartRecruiting_BackEnd.deeplearning.pre-process
import SmartRecruiting_BackEnd.deeplearning.cnn