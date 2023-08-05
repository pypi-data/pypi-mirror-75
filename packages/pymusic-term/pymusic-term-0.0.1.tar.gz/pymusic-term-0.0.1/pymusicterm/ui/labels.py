import py_cui

from pymusicterm.music import SongFile
from pymusicterm.util.file import File, FileMetadata

class SongInfoBlockLabel:

    _row:int=0
    _column:int=2
    _row_span:int=2
    _column_span:int=3
    _center:bool=False

    window:py_cui.widget_set.WidgetSet

    def __init__(self,window:py_cui.widget_set.WidgetSet):
        self.window=window
        self.block_label=self.window.add_block_label(self._initial_text(),self._row,self._column,
        row_span=self._row_span,column_span=self._column_span,center=self._center)

        self.__config()

    def _initial_text(self):
        file_path=File().get_file_path()
        text=""" Actual path: {}
        No Song Selected
        """.format(file_path)
        return text

    def set_song_info(self,song_file:SongFile):
        pass

    def __config(self):
        """ Function that configure the widget
        """
        self.block_label.set_color(py_cui.BLACK_ON_WHITE)
