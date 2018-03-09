import unittest

#add root directory to the path to import app
import sys
import os.path
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

sys.argv.append('-t')

from SmartRecruiting_BackEnd import app
from SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement import tokenize, preprocess, descriptor_to_string

app.config['stop_list'] = ['is', 'this', 'a', 'the']

test_text = 'Hello, this is a test.'

test_text_fr = 'Bonjour, je recherche un stagiaire en développement web pour un site web full-stack en Java et qui réponds aux besoins de notre client.'

test_desc = [np.array([0.1,0.2],dtype=float),np.array([0.3,0.4],dtype=float)]

class Test_user(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(tokenize(test_text), ['hello', 'test'])

    def test_same_descriptor(self) :
        desc1 = preprocess(test_text_fr)
        desc2 = preprocess(test_text_fr)
        for i in range(0, len(desc1)) :
            self.assertListEqual(list(desc1[i]),list(desc2[i]))

    def test_desc_to_string(self) :
        res = descriptor_to_string(test_desc)
        self.assertEqual(res, '[0.1 0.2],[0.3 0.4]')

if __name__ == '__main__':
    unittest.main()
