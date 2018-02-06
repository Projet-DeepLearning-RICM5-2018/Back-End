"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import SmartRecruiting_BackEnd.api.routes
import SmartRecruiting_BackEnd.data