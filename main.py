#!/usr/bin/env python3

'''
 ---------- main.py  ----------
 The primary running process of Inventify.
'''

__version__ = "0.1.0"

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window # For back button screen selecting
from kivy.base import EventLoop # For back button event capture

import kivy
import json

kivy.require('1.10.0')

# Set window size (360x640 for the demo device)
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Prevent kivy's automatic application exit on back button
Config.set('kivy', 'exit_on_escape', '0')

class PostInventionGridLayout(GridLayout):
    '''Kivy layout for the invention posting page'''

class SearchInventionsGridLayout(GridLayout):
    '''Kivy layout for the search inventions page'''

    displayed_inventions = [""] # no displayed inventions to start

    # Function called when search is pressed
    def search(self, searchText):
        '''Allows the user to search for inventions.'''

        search_result = DBAccess.searchQuery(self, searchText)

        if search_result["name"] not in self.displayed_inventions:
            button = Button(text=search_result["name"])
            #button.bind(on_release=app.screen_select('view_invention'))
            self.ids.button_grid.add_widget(button)
            self.displayed_inventions.append(search_result["name"])

    def populate(self):
        '''Populates the list of inventions'''

class ViewInventionGridLayout(GridLayout):
    '''Kivy layout for the invention viewing page'''

class DeveloperHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class InventorHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class EmptyLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class DBAccess():
    '''Database Access for interacting with the Inventify database.'''

    def searchQuery(self, search):
        '''Queries the database for inventions.
        :return: dictionary object of invention
        '''

        # temporary solution
        simulatedJSON = '{ "name":"Test Invention 1", "NDA":0, "description":"This is a description of the test invention. No NDA."}'
        return json.loads(simulatedJSON)

class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)
    root_screen = ObjectProperty(None)

class InventifyApp(App):
    '''This is the main running process within the app.'''

    def build(self):
        '''This method loads the root.kv file automatically
        :return: none
        '''
        # loading the content of root.kv
        self.root = Builder.load_file('kv_modes/root.kv')

        # hook_keyboard binds the escape key (back button in android)
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def screen_select(self, selector):
        '''
        :param selector: character that is dependant on which mode button is toggled.
        :return: none. Effect: Switches container to a different kv layout.
        '''

        filename = selector + '.kv'
        # unload the content of the .kv file
        # reason: may have data from previous calls
        Builder.unload_file('kv_modes/' + filename)
        # clear the container
        self.root.root_screen.clear_widgets()
        # load the .kv file
        selector = Builder.load_file('kv_modes/' + filename)
        # add content of the .kv file to the container
        self.root.root_screen.add_widget(selector)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.screen_select('root')
            return True


if __name__ == '__main__':
    '''Start the application'''

    InventifyApp().run()