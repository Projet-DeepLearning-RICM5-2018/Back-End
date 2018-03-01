# encoding: utf-8
# -*- coding: utf-8 -*-
"""
This script runs the SmartRecruiting_BackEnd application using a development server.
"""
import sys, locale, os
import codecs
from os import environ
from SmartRecruiting_BackEnd import app

if __name__ == '__main__':

    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555    
    
    app.run(HOST, PORT)
        