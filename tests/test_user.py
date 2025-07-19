#I tried to create the unit test but I am not very confident about it

import unittest
from app.user_class import user_class  # this line imports the user class

class TestAUser(unittest.TestCase):
    def test_that_user_is_admin(self): # unit test to check if the user role is admin
        self.assertTrue(user_class("admin", "admin").is_user_admin())
        self.assertFalse(user_class("john", "user").is_user_admin())
