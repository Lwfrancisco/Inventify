#!/usr/bin/env python3

'''
 ---------- main.py  ----------
 The primary running process of Inventify.
'''

__version__ = "0.1.1"

import kivy

import dbaccess as db
import invention as inv

kivy.require('1.10.0')

# Config.set should be invoked before importing any other kivy modules
# Set window size (360x640 for the demo device)
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Prevent kivy's automatic application exit on back button
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.base import EventLoop # For back button event capture


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
                button_text = str(i['name']) + " #" + str(i['id'])
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

        self.ids['name'].text = self.name + " #" + self.identifier
        self.ids['description'].text = "Description: \n" + self.description

        # Deactivate Accept NDA Button
        self.ids['nda_button'].disabled = True

class DeveloperHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class InventorHomeGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class NDAListGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

class ViewBasicNDAGridLayout(GridLayout):
    '''Contains class members accessible to the kv file'''

    def populate(self, file):

        # with open(file) as f:
            # self.ids['nda_text'].text = "stuff" + f.read()

        self.ids['nda_text'].text = """
Basic Nondisclosure Agreement
This Nondisclosure Agreement (the 'Agreement') is entered into by and between Insurgent Technologies ('Disclosing Party') and whomever it may concern ('Receiving Party') for the purpose of preventing the unauthorized disclosure of Confidential Information as defined below. The parties agree to enter into a confidential relationship with respect to the disclosure of certain proprietary and confidential information ('Confidential Information').

1. Definition of Confidential Information. For purposes of this Agreement, 'Confidential Information' shall include all information or material that has or could have commercial value or other utility in the business in which Disclosing Party is engaged. If Confidential Information is in written form, the Disclosing Party shall label or stamp the materials with the word 'Confidential' or some similar warning. If Confidential Information is transmitted orally, the Disclosing Party shall promptly provide a writing indicating that such oral communication constituted Confidential Information.

2. Exclusions from Confidential Information. Receiving Party's obligations under this Agreement do not extend to information that is: (a) publicly known at the time of disclosure or subsequently becomes publicly known through no fault of the Receiving Party; (b) discovered or created by the Receiving Party before disclosure by Disclosing Party; (c) learned by the Receiving Party through legitimate means other than from the Disclosing Party or Disclosing Party's representatives; or (d) is disclosed by Receiving Party with Disclosing Party's prior written approval.

3. Obligations of Receiving Party. Receiving Party shall hold and maintain the Confidential Information in strictest confidence for the sole and exclusive benefit of the Disclosing Party. Receiving Party shall carefully restrict access to Confidential Information to employees, contractors, and third parties as is reasonably required and shall require those persons to sign nondisclosure restrictions at least as protective as those in this Agreement. Receiving Party shall not, without prior written approval of Disclosing Party, use for Receiving Party's own benefit, publish, copy, or otherwise disclose to others, or permit the use by others for their benefit or to the detriment of Disclosing Party, any Confidential Information. Receiving Party shall return to Disclosing Party any and all records, notes, and other written, printed, or tangible materials in its possession pertaining to Confidential Information immediately if Disclosing Party requests it in writing.

4. Time Periods. The nondisclosure provisions of this Agreement shall survive the termination of this Agreement and Receiving Party's duty to hold Confidential Information in confidence shall remain in effect until the Confidential Information no longer qualifies as a trade secret or until Disclosing Party sends Receiving Party written notice releasing Receiving Party from this Agreement, whichever occurs first.

5. Relationships. Nothing contained in this Agreement shall be deemed to constitute either party a partner, joint venturer or employee of the other party for any purpose.

6. Severability. If a court finds any provision of this Agreement invalid or unenforceable, the remainder of this Agreement shall be interpreted so as best to effect the intent of the parties.

7. Integration. This Agreement expresses the complete understanding of the parties with respect to the subject matter and supersedes all prior proposals, agreements, representations, and understandings. This Agreement may not be amended except in a writing signed by both parties.

8. Waiver. The failure to exercise any right provided in this Agreement shall not be a waiver of prior or subsequent rights.

This Agreement and each party's obligations shall be binding on the representatives, assigns, and successors of such party. Each party has signed this Agreement through its authorized representative.
        """

    def open_pdf(self, filename):
        '''Opens pdf in external app'''

        from jnius import cast, autoclass # for access to android intents to open pdf
        # import urllib.parse as urlparse
        # import mimetypes

        # Intent = autoclass('android.content.Intent')
        # AndroidString = autoclass('java.lang.String')
        # Uri = autoclass('android.net.Uri')

        # PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity

        # url = "http://www.mountvernon.org/sites/mountvernon.org/files/images/GW_Stuart-CT-6437.jpg"
        # path = self.download_file(url)
        # mimetype = mimetypes.guess_type(path)[0]
        # pdf_uri = urlparse.urljoin('file://', path)

        # intent = Intent()
        # intent.setAction(Intent.ACTION_VIEW)
        # intent.setDataAndType(Uri.parse(pdf_uri), mimetype)
        # currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        # currentActivity.startActivity(intent)

        # import the needed Java class
        # PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # Intent = autoclass('android.content.Intent')
        # Uri = autoclass('android.net.Uri')

        # # create the intent
        # intent = Intent()
        # intent.setAction(Intent.ACTION_VIEW)
        # # intent.setData(Uri.parse('http://kivy.org'))
        # with open("nda/nda.txt") as file:
        #     intent.setData(Uri.fromFile(file), "text/html")

        # # PythonActivity.mActivity is the instance of the current Activity
        # # BUT, startActivity is a method from the Activity class, not from our
        # # PythonActivity.
        # # We need to cast our class into an activity and use it
        # currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        # currentActivity.startActivity(intent)

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