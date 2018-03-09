import unittest

#add root directory to the path to import app
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

sys.argv.append('-t')

from SmartRecruiting_BackEnd import app, dbManager
from SmartRecruiting_BackEnd.data import Base, User
from SmartRecruiting_BackEnd.data import init_db, dbSession as dB

class Test_user(unittest.TestCase):
    serialized_test_user = {'id':1,'name':'test_name','surname':'test_surname','role':'test_role','email':'test_email','password':'test_password','is_admin':True};

    def add_test_user(self):
        #Delete users and add one in the database
        dbManager.delete_users()
        user = User('test_name', 'test_surname', 'test_role', 'test_email', 'test_password', 1)
        user.id = 1
        dB.add(user)
        dB.commit()

    def test_get_all_users(self):
        self.add_test_user()
        self.assertEqual(dbManager.get_all_users(), [self.serialized_test_user])
        
    def test_get_user_by_id(self):
        self.add_test_user()
        self.assertEqual(dbManager.get_user_by_id(1), self.serialized_test_user)
        self.assertEqual(dbManager.get_user_by_id(36), None)

    def test_get_user_by_email(self):
        self.add_test_user()
        self.assertEqual(dbManager.get_user_by_email('test_email').serialize(), self.serialized_test_user)

    def test_get_one_admin(self):
        self.add_test_user()
        self.assertEqual(dbManager.get_one_admin().serialize(), self.serialized_test_user)

    def test_add_user(self):
        dbManager.delete_users()
        dbManager.add_user('test_name', 'test_surname', 'test_role', 'test_email', 'test_password', 1)
        self.assertEqual(len(dbManager.get_all_users()), 1)

    def test_update_user(self):
        self.add_test_user()
        self.assertEqual(dbManager.update_user(1, 'new_test_name', 'new_test_surname', 'new_test_role', 'new_test_email', 'new_test_password', 0), True)
        self.assertEqual(dbManager.get_user_by_id(1), {'id':1,'name':'new_test_name','surname':'new_test_surname','role':'new_test_role','email':'new_test_email','password':'new_test_password','is_admin':False})
        self.assertEqual(dbManager.update_user(36, 'new_test_name', 'new_test_surname', 'new_test_role', 'new_test_email', 'new_test_password', 0), None)

    def test_delete_user(self):
        self.add_test_user()
        self.assertEqual(dbManager.delete_user(1), True)
        self.assertEqual(len(dbManager.get_all_users()), 0)
        self.assertEqual(dbManager.delete_user(36), None)

    def test_delete_users(self):
        self.add_test_user()
        dbManager.delete_users()
        self.assertEqual(len(dbManager.get_all_users()), 0)

if __name__ == '__main__':
    unittest.main()
