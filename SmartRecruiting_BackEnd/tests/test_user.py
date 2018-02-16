import unittest
from SmartRecruiting_BackEnd.data import DatabaseManager, Base, User
from SmartRecruiting_BackEnd.data import init_db, dbSession as dB

dbManager = DatabaseManager()

class Test_user(unittest.TestCase):
    def test_get_all_users(self):
        dbManager.delete_users()
        user = User('test_name', 'test_surname', 'test_role', 'test_email', 'test_password', 1)
        user.id = 1
        dB.add(user)
        dB.commit()
        self.assertEqual(dbManager.get_all_users(), [{'id':1,'name':'test_name','surname':'test_surname','role':'test_role','email':'test_email','password':'test_password','is_admin':True}])
        
    def test_get_user_by_id(self):
        dbManager.delete_users()
        user = User('test_name', 'test_surname', 'test_role', 'test_email', 'test_password', 1)
        user.id = 1
        dB.add(user)
        dB.commit()
        self.assertEqual(dbManager.get_user_by_id(1), {'id':1,'name':'test_name','surname':'test_surname','role':'test_role','email':'test_email','password':'test_password','is_admin':True})

if __name__ == '__main__':
    unittest.main()
