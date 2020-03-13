#!/usr/bin/env python3

'''
 ---------- dbaccess.py  ----------
 File containing code to interact with Inventify's database. (currently just json)
'''

import json
import os
import invention as inv

# Class simulates DB by accessing JSON
class DBAccess():
    '''Database Access for interacting with the Inventify database.'''

    # default constructor
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        # Default data location
        self.filename = self.filepath + '/json/inventions.json'

        # Check if json file exists. If not, make one.
        if not os.path.isfile(self.filename):
            inv_list = {'inventions':[]}
            inv_list['id_count'] = 0

            # Create Directory for file
            directory = "json"
            path = os.path.join(self.filepath, directory) 
            os.mkdir(path)

            # Create file/add basic info
            with open(self.filename, 'w') as json_file:
                json.dump(inv_list, json_file, indent=4)
                json_file.close()

    # Search database with search query
    def searchQuery(self, search):
        '''Queries the database for inventions.
        :return: list of inventions (dictionary objects)
        '''
        
        with open(self.filename) as json_file:
            data = json.load(json_file)
            temp = data['inventions']

        # Inefficient as heck. Fix later.
        name_search = list(filter(lambda element: element['name'].lower().find(search.lower()) != -1, temp))
        desc_search = list(filter(lambda element: element['description'].lower().find(search.lower()) != -1, temp))
        id_search = list(filter(lambda element: str(element['id']).find(search) != -1, temp))
        results = list(name_search + desc_search + id_search)
        results = {frozenset(item.items()) : item for item in results}.values()
        return results

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


# inv1 = inv.invention("test", False, "Description for test", "test_user")
# obj1 = DBAccess()
# obj1.insertInvention(inv1)
# results = obj1.searchQuery('blah')
# print(results)