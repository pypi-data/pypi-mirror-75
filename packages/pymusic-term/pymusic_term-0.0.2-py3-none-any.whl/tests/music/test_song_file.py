import os
import unittest

from pymusicterm.music import SongFile,is_valid_extension

def join_path(path,file_name) -> str:
    return os.path.join(path,file_name)

class TestSongFile(unittest.TestCase):
    
    def setUp(self):
        self.win_path='C:\\Users\\MyName\Music'
        self.linux_path='/home/myuser/Music/'
        self.file_name='song.mp3'
        self.file_name2='song.wav'
        self.file_name3='song.mp4'

        self.win_song_file=SongFile(self.win_path,self.file_name)
        self.linux_song_file=SongFile(self.linux_path,self.file_name)

    def test_valid_extension(self):
        self.assertEqual(is_valid_extension(self.file_name),True)
        self.assertEqual(is_valid_extension(self.file_name2),True)
        self.assertEqual(is_valid_extension(self.file_name3),False)

    def test_get_name(self):
        self.assertEqual(self.win_song_file.get_name(),'song')
        self.assertEqual(self.linux_song_file.get_name(),'song')

    def test_get_file_path(self):
        self.assertEqual(self.win_song_file.get_file_path(),join_path(self.win_path,self.file_name))
        self.assertEqual(self.linux_song_file.get_file_path(),join_path(self.linux_path,self.file_name))

    def test_get_path(self):
        self.assertEqual(self.win_song_file.get_path(),self.win_path)
        self.assertEqual(self.linux_song_file.get_path(),self.linux_path)

    def tearDown(self):
        del(self.win_path)
        del(self.linux_path)
        del(self.file_name)

        del(self.win_song_file)
        del(self.linux_song_file)

if __name__ == "__main__":
    unittest.main()
