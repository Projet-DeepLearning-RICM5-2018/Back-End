import unittest

#add root directory to the path to import app
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

sys.argv.append('-t')

from SmartRecruiting_BackEnd import app
from SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement import *
from SmartRecruiting_BackEnd.data import DatabaseManager, Base
from SmartRecruiting_BackEnd.data import init_db, dbSession as dB

dbManager = DatabaseManager()

app.config['stop_list'] = ['is', 'this', 'a', 'the']

test_text = 'Hello, this is a test.'

class Test_user(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(tokenize(test_text), ['hello', 'test'])

if __name__ == '__main__':
    unittest.main()
