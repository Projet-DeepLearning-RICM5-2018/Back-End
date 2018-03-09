#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 10:20:01 2018

@author: Qianqian FU
"""

import unittest

#add root directory to the path to import app
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

sys.argv.append('-t')

from SmartRecruiting_BackEnd import app
from SmartRecruiting_BackEnd.data import DatabaseManager, Base, Offer
from SmartRecruiting_BackEnd.data import init_db, dbSession as dB

dbManager = DatabaseManager()

class Test_offer(unittest.TestCase):
    serialized_test_offer = {'id':1,'title':'test_title','content':'test_content','descriptor':'test_descriptor','id_offer':2};

    def add_test_offer(self):
        #Delete offers and add one in the database
        dbManager.delete_offers()
        offer = Offer('test_title', 'test_content', 'test_descriptor', 2)
        offer.id = 1
        dB.add(offer)
        dB.commit()

    def test_get_all_offers(self):
        self.add_test_offer()
        self.assertEqual(dbManager.get_all_offers(), [self.serialized_test_offer])
        
    
    def test_get_offer_by_id(self):
        self.add_test_offer()
        self.assertEqual(dbManager.get_offer_by_id(1), self.serialized_test_offer)
        self.assertEqual(dbManager.get_offer_by_id(36), None)

    def test_add_offer(self):
        dbManager.delete_offers()
        dbManager.add_offer('test_title', 'test_content', 'test_descriptor', 2)
        self.assertEqual(len(dbManager.get_all_offers()), 1)

    def test_add_offer_v2(self):
        dbManager.delete_offers()
        dbManager.add_offer_v2('test_title', 'test_content', 'test_descriptor', 2)
        self.assertEqual(len(dbManager.get_all_offers()), 1)

    def add_offer_link_field(self):
        dbManager.delete_offers()
        dbManager.add_offer_link_field('test_title', 'test_content', 2,3,True)
        self.assertEqual(len(dbManager.get_all_offers()), 1)

    def test_update_offer(self):
        self.add_test_offer()
        self.assertEqual(dbManager.update_offer(1, 'new_test_title', 'new_test_content', 'new_test_descriptor', 2), True)
        self.assertEqual(dbManager.get_offer_by_id(1), {'id':1,'title':'new_test_title','content':'new_test_content','descriptor':'new_test_descriptor','id_user':2})
        self.assertEqual(dbManager.update_offer(36, 'new_test_title', 'new_test_content', 'new_test_descriptor', 0), None)

    def test_delete_offer(self):
        self.add_test_offer()
        self.assertEqual(dbManager.delete_offer(1), True)
        self.assertEqual(len(dbManager.get_all_offers()), 0)
        self.assertEqual(dbManager.delete_offer(36), None)

    def test_delete_offers(self):
        self.add_test_offer()
        dbManager.delete_offers()
        self.assertEqual(len(dbManager.get_all_offers()), 0)

if __name__ == '__main__':
    unittest.main()