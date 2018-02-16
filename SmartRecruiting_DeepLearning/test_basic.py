#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import unittest
import csv

import pretraiterCSV#, word2vec_basic

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

if __name__ == "__main__":
    unittest.main()
