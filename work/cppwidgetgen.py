'''
Created on Jul 14, 2021

@author: fstuffdev
'''
from work.cppgen import * 

def generateWidgetsHeader(filepath):
    
    template = "templates/LvWidgets.h"
    fileScan = os.listdir(filepath)
    headerToInclude = open("LvWidgets_temp", "a")
    if(headerToInclude):
        for file in fileScan:
            fname = filepath + file
            file_name, file_extension = os.path.splitext(fname)
            if(file_extension == ".h"):
                headerToInclude.write("\n" + '#include "' + file + '" ')
        headerToInclude.close()
        
        headerToInclude = open("LvWidgets_temp", "r")
        hppTemplate = open(template, "r")
        
        hpp = headerToInclude.read()
        hppTemp = hppTemplate.read()
        
        hppTemp = hppTemp.replace("/*WINCLUDES*/", hpp)
        
        headerOutFile = os.path.join(filepath,"LvWidgets.h")
                
        hppOut = open(headerOutFile, "w")
        hppOut.write(hppTemp)
        
        headerToInclude.close()
        hppTemplate.close()
        hppOut.close()
        
        os.remove("LvWidgets_temp")
       

class CppWidgetGenerator(CppGenerator):
    
    def __init__(self):
        super().__init__()
    
    def fgood_check_condition(self,f_decl,f_name, pidx ,pname, ptype):
        fgood = False
        
        if(pidx == 0 and (self.name in f_name) 
           and (pname == "obj" or pname == self.name) 
           and (ptype == "lv_obj_t" or ptype == "lv_obj_t *" or ptype == "lv_obj_t*" or 
                ptype == "const lv_obj_t" or ptype == "const lv_obj_t *" or ptype == "const lv_obj_t*"
               )): 
            fgood = True
   
        return fgood
            
        
    def set_template_fname(self,template_fname = None):
        self.template = "templates/LvObj"
        if(self.name != "obj"):
            self.template = "templates/LvWidget"
            
            
    def template_replace_cpp(self, cpp, cppMeth):
        cpp = cpp.replace("/*METHODS*/", cppMeth)
        if(self.name != "obj"):
            cpp = cpp.replace("/*WNAME*/", self.objName)
            cpp = cpp.replace("/*WCAP*/", self.name.upper())
        return cpp
    
    def template_replace_hpp(self, hpp, hppMeth):
        hpp = hpp.replace("/*METHODS*/", hppMeth)
        if(self.name != "obj"):
            hpp = hpp.replace("/*WNAME*/", self.objName)
            hpp = hpp.replace("/*WCAP*/", self.name.upper())
        return hpp
            
            
            
            
            
            
            