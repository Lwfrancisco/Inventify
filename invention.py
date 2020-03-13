#!/usr/bin/env python3

'''
 ---------- invention.py  ----------
 File for creating/standardizing invention objects.
'''

def invention(name, NDA, desc, username, id=0):
    '''Returns invention dictionary'''

    return {"id":id, "name":name, "NDA":NDA, "description":desc, "username":username}