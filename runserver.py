"""
This script runs the SmartRecruiting_BackEnd application using a development server.
"""
import os
import sys
from os import environ
from SmartRecruiting_BackEnd import app
from SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement import test
if __name__ == '__main__':
    
    
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    if(app.config['INIT']):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        test()
    else:
        app.run(HOST, PORT)
        