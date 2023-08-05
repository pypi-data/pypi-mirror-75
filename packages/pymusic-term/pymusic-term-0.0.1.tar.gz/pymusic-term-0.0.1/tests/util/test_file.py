import unittest

from pymusicterm.util.system import get_user_name
from pymusicterm.util.file import File

class TestFile(unittest.TestCase):

    def setUp(self):
        self.file_class=File()
        self.username=get_user_name()
        self.win_path='C:\\Users\\{}\Music'.format(self.username)
        self.linux_path='/home/{}/Music'.format(self.username)

    def test_get_default_path(self):
        self.assertIn(self.file_class.get_file_path(),[self.win_path,self.linux_path])

    def test_set_file_path(self):
        # Set default file path for windows
        self.file_class.set_file_path(self.win_path)
        self.assertEqual(self.file_class.get_file_path(),self.win_path)

        # Set default file path for linux
        self.file_class.set_file_path(self.linux_path)
        self.assertEqual(self.file_class.get_file_path(),self.linux_path)

    def tearDown(self):
        del(self.file_class)
        del(self.username)
        del(self.win_path)
        del(self.linux_path)

if __name__ == "__main__":
    unittest.main()
