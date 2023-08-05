import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
import threading
from pygame import mixer
from typing import List

from pymusicterm.music import SongFile
# https://www.thecodingpup.com/post_detailed/music-player-in-python
class MusicPlayer:
    """ Music player using pygame

    This class uses pygame as a player, which contains functions to control the music. Some 
    of this actions are pause, stop, volume up or down, add or remove song in queue, etc.
    """

    FADE_OUT_TIME:int = 500
    PLAYER_STOPPED:int=0
    NO_QUEUE_SONGS:int=1
    SONG_PLAYING:int=2
    SONG_STOPPED:int=3
    SONG_CHANGING:int=4

    _song_file:SongFile = None
    _queue_songs:List[SongFile] = []
    _main_thread:threading.Thread=None
    _song_index:int = 0
    _status:int=None

    paused:bool=False

    def __init__(self):
        """ Constructor for MusicPLayer
        """
        mixer.init() #Initialize pygame

    def not_in_queue_songs(self,song_file:SongFile) -> bool:
        """Fuction to check if a SongFile that's added already exists in queue songs

        Parameters
        ----------
        song_file : SongFile
            Dataclass where the info of the song file

        Returns
        -------
        exists : bool
            returns if exists
        """
        if not any(song.get_file_path()==song_file.get_file_path() for song in self._queue_songs):
            return True
        return False

    def add_song(self,song_file:SongFile):
        """Adds a SongFile to the queue songs

        Parameters
        ----------
        song_file : SongFile
            Dataclass where the info of the song file
        """
        # TODO: This code can be reduce
        if not self._queue_songs:
            self._status=self.SONG_PLAYING
            self._song_file=song_file # Sets actual SongFile playing
            mixer.music.load(self._song_file.get_file_path()) # Loads the song and play it automatically
            mixer.music.play()
            self._check_player()

        self._queue_songs.append(song_file) # Song added to queue songs

    def remove_song(self, index:int):
        """ Removes song from queue

        Parameters
        ----------
        index : int
            Index of item in queue songs menu
        """
        try:
            if index == self._song_index:
                pass
            else:
                del self._queue_songs[index]
        except IndexError:
            pass

    def play_song(self,index:int):
        """ Function that plays a song in queue songs

        Parameters
        ----------
        index : int
            Index of item in queue songs menu
        """
        self._status=self.SONG_CHANGING
        # Validate if actual song is playing
        if self._song_index != index: # TODO: Add file path comparison
            self._song_index=index # Sets new index of new song playing
            mixer.music.fadeout(self.FADE_OUT_TIME) # Fadeout until it stops
            mixer.music.load(self._queue_songs[index].get_file_path()) # Loads the song and play it automatically
            mixer.music.play()
        else:
            mixer.music.rewind()
        if self._status==self.NO_QUEUE_SONGS:
            # If every song was played, it will restrart the thread and change status
            self._status=self.SONG_PLAYING #FIXME: Thread doesn't restart
            self._check_player()
        self._status=self.SONG_PLAYING

    def previous_song(self):
        """ Plays previous song in queue
        """
        self._status=self.SONG_STOPPED
        index = self._song_index - 1
        self.play_song(index)

    def next_song(self):
        """ Plays next song in queue
        """
        self._status=self.SONG_STOPPED
        index= self._song_index + 1
        self.play_song(index)

    def pause_song(self):
        """ Pauses the song playing
        """
        if self.paused:
            self.paused=False
            mixer.music.unpause()
        else:
            self.paused=True
            mixer.music.pause()

    def is_playing(self) -> bool:
        """ Return the current state of the mixer (if is busy)

        Return
        ------
        get_busy : bool
            Check if the music stream is playing
        """
        return mixer.music.get_busy()

    def get_song_index(self) -> int:
        """ Gets actual index of the list of queue songs

        Returns
        -------
        song_index : int
            Actual index
        """
        return self._song_index

    def get_queue_songs(self) -> List[str]:
        """ Gets the list of queue songs

        Returns
        -------
        queue_songs : List[str]
            Queue songs
        """
        return self._queue_songs

    def stop_song(self):
        """ Function that stops actual song
        """
        if self._main_thread is not None:
            self._status=self.PLAYER_STOPPED
            self._main_thread.join()
        mixer.music.fadeout(self.FADE_OUT_TIME)

    def auto_play(self):
        """ Function that automatically changes the song playing or stops the main_thread
        """
        max_index=len(self._queue_songs)-1

        #TODO: Handle when queue song list is empty and after the song stopped playing is added a new song

        # Will check if is the last song and it stills playing
        if self._song_index < max_index and self._status != self.SONG_CHANGING: 
            self.next_song()

        if self._song_index == max_index and self._status==self.SONG_PLAYING:
            self._status=self.NO_QUEUE_SONGS

    def _check_player(self):
        """ Function that starts a thread to change automatically the song
        """
        def check_player_thread():
            """ Child function that will be runned in a thread
            """
            while self._status!=self.PLAYER_STOPPED and self._status!=self.NO_QUEUE_SONGS:
                if not self.is_playing():
                    self.auto_play()

        self._main_thread=threading.Thread(name="Check Player Thread",target=check_player_thread)
        self._main_thread.start()
