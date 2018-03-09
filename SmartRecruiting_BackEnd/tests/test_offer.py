import unittest

#add root directory to the path to import app
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

sys.argv.append('-t')

from SmartRecruiting_BackEnd import app, dbManager
from SmartRecruiting_BackEnd.data import Base, User, Field, Offer
from SmartRecruiting_BackEnd.data import init_db, dbSession as dB

class Test_user(unittest.TestCase):
    serialized_test_offer = {'id':1,'title':'test_title','content':'test_content','descriptor':'test_descriptor','id_user':1};

    def add_test_user(self):
        User.query.delete()
        user = User('test_name', 'test_surname', 'test_role', 'test_email', 'test_password', 1)
        user.id = 1
        dB.add(user)
        dB.commit()

    def add_test_field(self):
        Field.query.delete()
        field = Field('test_name', 'test_description', 'test_descriptor', 'test_website')
        field.id = 1
        dB.add(field)
        dB.commit()

    def add_test_offer(self):
        #Delete offers and add one in the database
        Offer.query.delete()
        self.add_test_user()
        
        offer = Offer('test_title', 'test_content', 'test_descriptor', 1)
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
        Offer.query.delete()
        self.add_test_user()
        dbManager.add_offer('test_title', 'test_content', 'test_descriptor', 1)
        self.assertEqual(len(dbManager.get_all_offers()), 1)

    def add_offer_link_field(self):
        Offer.query.delete()
        self.add_test_user()
        self.add_test_field()
        dbManager.add_offer_link_field('test_title', 'test_content', 1, 1, True)
        self.assertEqual(len(dbManager.get_all_offers()), 1)

    def test_update_offer(self):
        user = User('test_name2', 'test_surname2', 'test_role2', 'test_email2', 'test_password2', 1)
        user.id = 2
        dB.add(user)
        dB.commit()
        self.add_test_offer()
        self.assertEqual(dbManager.update_offer(1, 'new_test_title', 'new_test_content', 'new_test_descriptor', 2), True)
        self.assertEqual(dbManager.get_offer_by_id(1), {'id':1,'title':'new_test_title','content':'new_test_content','descriptor':'new_test_descriptor','id_user':2})
        self.assertEqual(dbManager.update_offer(36, 'new_test_title', 'new_test_content', 'new_test_descriptor', 2), None)

    def test_delete_offer(self):
        self.add_test_offer()
        self.assertEqual(dbManager.delete_offer(1), True)
        self.assertEqual(len(dbManager.get_all_offers()), 0)
        self.assertEqual(dbManager.delete_offer(36), None)

if __name__ == '__main__':
    unittest.main()

