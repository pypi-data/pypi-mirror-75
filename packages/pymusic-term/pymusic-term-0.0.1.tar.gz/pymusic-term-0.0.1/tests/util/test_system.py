import getpass
import platform
import unittest

from pymusicterm.util.system import get_platform_name,get_user_name

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.platform_name:str=platform.system()
        self.username:str=getpass.getuser()

    def test_get_platform(self):
        self.assertEqual(get_platform_name(),self.platform_name.lower())
        self.assertNotEqual(get_platform_name(),self.platform_name)
        self.assertNotEqual(get_platform_name(),'WINDOWS')
        self.assertNotEqual(get_platform_name(),'LINUX')
    
    def test_get_username(self):
        self.assertEqual(get_user_name(),self.username)
        self.assertNotEqual(get_user_name(),'username')
    
    def tearDown(self):
        del(self.platform_name)
        del(self.username)

if __name__ == "__main__":
    unittest.main()
