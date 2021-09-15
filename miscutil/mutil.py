'''
Created on Aug 9, 2021

@author: fstuffdev
'''

from re import sub
# function to convert string to camelCase
def camelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]
