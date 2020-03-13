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

import dbaccess as db
import invention as inv

kivy.require('1.10.0')

# Set window size (360x640 for the demo device)
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Prevent kivy's automatic application exit on back button
Config.set('kivy', 'exit_on_escape', '0')

class PostInventionGridLayout(GridLayout):
    '''Kivy layout for the invention posting page'''

    def post(self, name, desc, nda, user="test_user"):
        if nda == "down":
            nda = True
        else:
            nda = False
        post = inv.invention(name, nda, desc, user)
        database.insertInvention(post)

class SearchInventionsGridLayout(GridLayout):
    '''Kivy layout for the search inventions page'''

    # Function called when search is pressed
    def search(self, searchText):
        '''Allows the user to search for inventions.'''

        self.ids.button_grid.clear_widgets()
        displayed_inventions = [] # no displayed inventions to start

        search_results = list(database.searchQuery(searchText))

        # print(type(search_results[0]['id']))

        for i in search_results:
            if i['id'] not in displayed_inventions:
                button_text = "id: " + str(i['id']) + " Name: " + str(i['name'])
                button = Button(text=button_text, id=str(i['id']))
                self.ids.button_grid.add_widget(button)
                button.bind(on_release=self.populate)
                displayed_inventions.append(i['id'])

    def populate(self, instance):
        '''Populates the list of inventions'''

        root.inv_id = int(instance.id)
        root.screen_select('view_invention')

    def get_id(self,  instance):
        for id, widget in instance.parent.ids.items():
            if widget.__self__ == instance:
                return id

class ViewInventionGridLayout(GridLayout):
    '''Kivy layout for the invention viewing page'''

    name = ''
    description = ''
    identifier = ''

    def populate(self):
        print(root.inv_id)
        invention = database.id_query(root.inv_id)[0]
        print(invention)

        self.name = invention['name']
        self.description = invention['description']
        self.identifier = str(invention['id'])

        self.ids['name'].text = self.name
        self.ids['description'].text = "Description: \n" + self.description
        self.ids['identifier'].text = "ID: " + self.identifier

class DeveloperHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class InventorHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class EmptyLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)
    root_screen = ObjectProperty(None)

class InventifyApp(App):
    '''This is the main running process within the app.'''

    screen_stack = []

    def build(self):
        '''This method loads the root.kv file automatically
        :return: none
        '''
        # loading the content of root.kv
        self.root = Builder.load_file('kv_modes/root.kv')

        # Push root onto stack
        self.screen_stack.append('root')

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
        # add screen to screen stack
        self.screen_stack.append(selector)
        # load the .kv file
        selector = Builder.load_file('kv_modes/' + filename)
        # add content of the .kv file to the container
        self.root.root_screen.add_widget(selector)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.go_back()
            return True

    def go_back(self):
            self.screen_stack.pop() # pop current screen

            if not self.screen_stack:           # if list is empty, exit application
                self.screen_select('')
            else:                               # else, go to last screen
                self.screen_select(self.screen_stack.pop())


if __name__ == '__main__':
    '''Start the application'''

    database = db.DBAccess()

    # Check if json file exists. If it does
    if len(database.searchQuery('test')) < 5:
        for i in range(0, 5):
            invention = inv.invention("Test " + str(i), i%2 == 0, "Description of invention...", "test_user")
            database.insertInvention(invention)

    
    # Temporary to figure out proper parameters passing between screens.
    inv_id = 0

    root = InventifyApp()

    root.run()