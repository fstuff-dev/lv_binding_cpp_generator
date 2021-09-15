'''
Created on Sep 10, 2021

@author: fstuffdev
'''

from work.cppgenericgen import * 

class CppTimerGenerator(CppGenericGenerator):
   
    def __init__(self):
        super().__init__()
                
    def deallocator(self):
        self.free = "lv_timer_del"
        
    def allocator(self):
        self.alloc = "lv_timer_create_basic()"  
        
        
