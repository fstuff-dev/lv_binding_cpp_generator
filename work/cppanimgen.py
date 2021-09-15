'''
Created on Sep 10, 2021

@author: fstuffdev
'''

from work.cppgenericgen import * 

class CppAnimGenerator(CppGenericGenerator):
   
    def __init__(self):
        super().__init__()
        
    def postInit(self):
        self.postinit = "init();"     
