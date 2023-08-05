import os

MUSIC_EXTENSIONS=(".mp3",".wav") # Valid music extensions

def is_valid_extension(file_name:str):
    if file_name.endswith(MUSIC_EXTENSIONS):
        return True
    return False

class SongFile:
    """ Class that stv  ores information of a song file

    This class with store the path where is found the song and the name
    of the file. And with the functions will return some requested information
    store.
    """
    _path:str
    _file_name:str

    def __init__(self,path:str,file_name:str):
        self._path=path
        self._file_name=file_name

    def get_name(self) -> str:
        """ Gets the name of the file

        Return
        ------
        name : str
            Name of the file (without extension)
        """
        return os.path.splitext(self._file_name)[0]

    def get_file_path(self) -> str:
        """ Gets the complete file path where is the song

        Return
        ------
        file_path : str
            Join of the path and file_name, for the location of the song file
        """
        return os.path.join(self._path,self._file_name)

    def get_path(self) -> str:
        """ Gets the path where is found the song file

        Return
        ------
        path : str
            Path where you can find the song
        """
        return self._path
