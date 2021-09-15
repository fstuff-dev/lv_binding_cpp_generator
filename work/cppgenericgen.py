'''
Created on Sep 6, 2021

@author: fstuffdev
'''

from work.cppgen import * 

class CppGenericGenerator(CppGenerator):
   
    def __init__(self):
        super().__init__()    
    
    def fgood_check_condition(self,f_decl,f_name, pidx ,pname, ptype):
        fgood = False
        
        if(pidx == 0 and (self.name in f_name) 
           and (pname == self.altname or pname == self.name) 
           and (ptype == "lv_{0}_t".format(self.name) or ptype == "lv_{0}_t *".format(self.name) or ptype == "lv_{0}_t*".format(self.name) or 
                ptype == "const lv_{0}_t".format(self.name) or ptype == "const lv_{0}_t *".format(self.name) or ptype == "const lv_{0}_t*".format(self.name)
               )): 
            fgood = True
   
        return fgood
        
    def set_template_fname(self,template_fname = None):
        self.template = "templates/LvGeneric"
                       

    
    def deallocator(self):
        self.free = "lv_mem_free"
        
    def allocator(self):
        self.alloc = "(lv_/*WTYPE*/_t*)lv_mem_alloc(sizeof(lv_/*WTYPE*/_t))"
        
    def postInit(self):
        self.postinit = ""   
        
        
    def template_replace_cpp(self, cpp, cppMeth):
        
        self.deallocator()
        self.allocator()
        self.postInit()
        
        cpp = cpp.replace("/*METHODS*/", cppMeth)
        cpp = cpp.replace("/*WNAME*/", self.objName)
        cpp = cpp.replace("/*WCAP*/", self.name.upper())
        cpp = cpp.replace("/*WALLOC*/",self.alloc )       
        cpp = cpp.replace("/*WTYPE*/", self.name)
        cpp = cpp.replace("/*WPOSTINIT*/", self.postinit)

        return cpp
    
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
        
        includes = '#include ""'
        hpp = hpp.replace("/*WINCLUDE*/","" )
        
        return hpp