import py_cui
from typing import List

from py_cui import widget_set

class LocalPlayerSettingsMenu:

    MENU_OPTIONS:List[str]=["Repeat All","Repeat Once","Shuffle"]
    TITLE:str="Player Settings"
    ROW:int=4
    COLUMN:int=0
    ROW_SPAN:int=2
    COLUMN_SPAN:int=2

    window:py_cui.widget_set.WidgetSet

    def __init__(self,window:py_cui.widget_set.WidgetSet) -> None:
        """ Constructor of LocalPlayerSettingsMenu class
        """
        self.window=window

        self.menu=self.window.add_checkbox_menu(self.TITLE,self.ROW,self.COLUMN,
        self.ROW_SPAN,self.COLUMN_SPAN)

        self.__config()

    def __config(self):
        """ Function that configures the CheckBoxMenu widget
        """
        self.menu.add_item_list(self.MENU_OPTIONS)

        self.menu.add_text_color_rule("X",py_cui.GREEN_ON_BLACK,'contains',match_type='regex')
        self.menu.set_focus_text("|Enter - Enable/Disable setting|")
    
    def create(self) -> py_cui.widgets.CheckBoxMenu:
        """ Function that returns the CheckBoxMenu Widget created

        Returns
        -------
        menu : CheckBoxMenu
            Return a CheckBoxMenu Widget
        """
        return self.menu

class LocalPlayerQueueMenu:
    
    TITLE="Songs queue"
    ROW:int=0
    COLUMN:int=0
    ROW_SPAN:int=4
    COLUMN_SPAN:int=2

    window:py_cui.widget_set.WidgetSet

    def __init__(self,window:py_cui.widget_set.WidgetSet) -> None:
        """ Constructor of LocalPlayerQueueMenu class
        """
        self.window=window

        self.menu=self.window.add_scroll_menu(self.TITLE,self.ROW,self.COLUMN,
        self.ROW_SPAN,self.COLUMN_SPAN)

        self.__config()

    def __config(self):
        """ Function that configures the ScrollMenu widget
        """
        self.menu.set_focus_text("| Backspace - Remove song | Enter - Play Song")

    def create(self) -> py_cui.widgets.ScrollMenu:
        """ Function that returns the ScrollMenu Widget created

        Returns
        -------
        menu : ScrollMenu
            Return a ScrollMenu Widget
        """
        return self.menu

class LocalPlayerSongsMenu:

    TITLE="Song Files List"
    ROW:int=3
    COLUMN:int=2
    ROW_SPAN:int=3
    COLUMN_SPAN:int=3

    window:py_cui.widget_set.WidgetSet

    def __init__(self,window:py_cui.widget_set.WidgetSet) -> None:
        """ Constructor of LocalPlayerSongsMenu class
        """
        self.window=window

        self.menu=self.window.add_scroll_menu(self.TITLE,self.ROW,self.COLUMN,
        self.ROW_SPAN,self.COLUMN_SPAN)
        
        self.__config()

    def __config(self):
        """ Function that configures the ScrollMenu widget
        """
        pass

    def create(self) -> py_cui.widgets.ScrollMenu:
        """ Function that returns the ScrollMenu widget created

        Returns
        -------
        menu : ScrollMenu
            Returns a ScrollMenu widget
        """
        return self.menu
