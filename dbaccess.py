#!/usr/bin/env python3

'''
 ---------- dbaccess.py  ----------
 File containing code to interact with Inventify's database. (currently just json)
'''

import json
import os.path
import invention as inv

# Class simulates DB by accessing JSON
class DBAccess():
    '''Database Access for interacting with the Inventify database.'''

    # default constructor
    def __init__(self):
        # Default data location
        self.filename = './json/inventions.json'

        # Check if json file exists. If not, make one.
        if not os.path.isfile(self.filename):
            inv_list = {"inventions":[]}
            inv_list['id_count'] = 0
            with open(self.filename, 'w') as json_file:
                json.dump(inv_list, json_file, indent=4)
                json_file.close()

    # Search database with search query
    def searchQuery(self, search):
        '''Queries the database for inventions.
        :return: dictionary object of invention
        '''

        # temporary solution
        simulatedJSON = '{ "name":"Test Invention 1", "NDA":0, "description":"This is a description of the test invention. No NDA."}'
        return json.loads(simulatedJSON)

    # Insert invention into database
    def insertInvention(self, invention):
        '''Inserts invention into database.'''

        # Read inventions list into program.
        with open(self.filename, 'r') as json_infile:
            data = json.load(json_infile)
            temp = data['inventions']
            id = data['id_count']
            json_infile.close()

        # Write updated inventions list to json file.
        with open(self.filename, 'w') as json_outfile:
            id = id + 1
            invention['id'] = id
            data['id_count'] = id
            temp.append(invention) # add invention to inventions list.
            json.dump(data, json_outfile, indent=4)
            json_outfile.close()