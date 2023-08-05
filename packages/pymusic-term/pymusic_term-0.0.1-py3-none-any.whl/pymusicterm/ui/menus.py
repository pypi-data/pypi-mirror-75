import py_cui
from typing import List

class LocalPlayerSettingsMenu:

    MENU_OPTIONS:List[str]=["Repeat All","Repeat Once","Shuffle"]
    TITLE:str="Player Settings"
    ROW:int=4
    COLUMN:int=0
    ROW_SPAN:int=2
    COLUMN_SPAN:int=2

    window:py_cui.widget_set.WidgetSet

    def __init__(self,window:py_cui.widget_set.WidgetSet):
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

        self.menu.set_focus_text("|Enter - Enable/Disable setting|")
    
    def create(self) -> py_cui.widgets.CheckBoxMenu:
        """ Function that return a CheckBoxMenu Widget

        Returns
        -------
        menu : CheckBoxMenu
            Return a CheckBoxMenu Widget
        """
        return self.menu
