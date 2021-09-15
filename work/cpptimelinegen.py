'''
Created on Sep 10, 2021

@author: fstuffdev
'''

from work.cppgenericgen import * 

class CppTimelineGenerator(CppGenericGenerator):
   
    def __init__(self):
        super().__init__()
                
    def deallocator(self):
        self.free = "lv_anim_timeline_del"
        
    def allocator(self):
        self.alloc = "lv_anim_timeline_create()"  
        
    def template_replace_hpp(self, hpp, hppMeth):
        
        self.deallocator()
        self.allocator()
        self.postInit()
        
        hpp = hpp.replace("/*METHODS*/", hppMeth)
        hpp = hpp.replace("/*WNAME*/", self.objName)
        hpp = hpp.replace("/*WCAP*/", self.name.upper())
        hpp = hpp.replace("/*WDELETE*/",self.free )
        hpp = hpp.replace("/*WTYPE*/", self.name)
        hpp = hpp.replace("/*WPRIVATE*/","" )
        
        includes = '#include "LvAnim.h"'
        hpp = hpp.replace("/*WINCLUDE*/",includes)
        
        return hpp
