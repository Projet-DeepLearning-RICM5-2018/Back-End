#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Created on 16th Feb 2018
@author: Qianqian
'''
import os
import unittest
import csv

import pretraiterCSV, word2vec_basic

class BasicTests(unittest.TestCase):
    ###############
    #### tests ####
    ###############

    # executed prior to each test
    def test_pretraiter(self):
        test='• text ·       not ()'
        resultat=['text not']
        pretraiterCSV.pretraiter(test)
        self.assertEqual(resultat, pretraiterCSV.pretraiter(test))

    def test_build_dataset(self):
        test=['long','ago','the','take','to','what','could','take','to']
        voc_size=7
        

if __name__ == "__main__":
    unittest.main()
