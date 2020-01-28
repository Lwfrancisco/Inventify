#!/usr/bin/env python3

# ---------- main.py  ----------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button

import kivy
import json

kivy.require('1.10.0')

class SearchInventionsGridLayout(GridLayout):

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    #     for child in reversed(self.ids.button_grid.children):
    #         if isinstance(child, Button):
    #             child.disabled = True
    #             child.opacity = 0

    # Function called when search is pressed
    def search(self, searchText):
        '''Allows the user to search for inventions.'''

        result = DBAccess.searchQuery(self, searchText)
        print(result["name"])


    
        # for child in reversed(self.ids.button_grid.children):
        #     if isinstance(child, Button) and child.text == :

        button = Button(text=result["name"])
        self.ids.button_grid.add_widget(button)

        # Iterate across the children "buttons" and populate them with information obtained.
        # for child in reversed(self.ids.button_grid.children):
        #     if isinstance(child, Button):
        #         child.text = result["name"]
        #         child.disabled = not child.disabled
        #         child.opacity = 0 if (child.opacity == 1) else 1
        #         # if child.disabled:
        #         #     child.opacity = 0
        #         # else:
        #         #     child.opacity = 1
        #         #     print(child.text)
        #         # child.opacity = 0 if child.disabled else 1



    def populate(self):
        '''Populates the list of inventions'''

class DeveloperHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class InventorHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)


class InventifyApp(App):
    '''This is the main running process within the app.'''

    def build(self):
        '''This method loads the root.kv file automatically
        :return: none
        '''
        # loading the content of root.kv
        self.root = Builder.load_file('kv_modes/root.kv')

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
        self.root.container.clear_widgets()
        # load the .kv file
        selector = Builder.load_file('kv_modes/' + filename)
        # add content of the .kv file to the container
        self.root.container.add_widget(selector)

class DBAccess():
    '''Database Access layer for interacting with the Inventify database.'''

    def searchQuery(self, search):
        '''Queries the database for inventions.
        :return: dictionary object of invention
        '''
        simulatedJSON = '{ "name":"Test Invention 1", "NDA":0, "description":"This is a description of the test invention. No NDA."}'
        return json.loads(simulatedJSON)


if __name__ == '__main__':
    '''Start the application'''

    InventifyApp().run()