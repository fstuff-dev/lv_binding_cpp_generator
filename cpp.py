'''
@author: fstuff-dev
'''

import sys
import os

from pycparser import c_ast, c_generator, parse_file
from pycparser.c_generator import CGenerator
from util import *
from copy import deepcopy
from string import Template
import shutil


################################################################ BASE GENERATOR ###########################################################
class CppGenerator(c_ast.NodeVisitor):
    
    # Constructor
    def __init__(self):
        self.cgen = CGenerator()
        self.libc = ""
        self.name = ""
        self.altname = ""
        self.classname = ""
        self.uppername = ""
        self.cpp_temp = ""
        self.hpp_temp = ""
        self.template_cpp = "LvGeneric.cpp"
        self.template_hpp = "LvGeneric.h"
        self.fname = ""
        
    # Scan a file
    def scan(self, filename):
        printv(f"Scanning file: {filename}")
        self.filename = filename
        ast = parse_file(self.filename,
                              use_cpp=True,
                              cpp_path='gcc',
                              cpp_args=['-nostdinc', '-E' , '-DPYCPARSER' , '-I' + self.libc]
                              )
        self.visit(ast)
     
    # Set libc path   
    def setlibc(self,libc):
        self.libc = libc
    
    # Set the name of the object to generate    
    def setname(self,name):
        self.name = name
        self.classname  = "Lv" + (name.replace("_"," ").title()).replace(" ","")
        self.uppername = self.name.upper()
        
    # Set the alternate name of the object to generate    
    def setalt(self,alternate):
        self.altname = alternate
    
    # Generate the class    
    def generate(self,opath):
        hpp,cpp = self.compose_class()
        self.write(opath,hpp,cpp)
        pass
    
    # Generate the class    
    def write(self,opath,hpp,cpp):
        printv(f"Writing: {self.classname}")
        if(hpp):
            file = open(os.path.join(opath,self.classname + ".h"),"w")
            if(file):
                file.write(hpp)
                file.close()
        if(cpp):
            file = open(os.path.join(opath,self.classname + ".cpp"),"w")
            if(file):
                file.write(cpp)
                file.close()
        pass
  
    # The function can be added to class if this method return true
    def func_good(self, f_decl):
        f_name = f_decl.name
        fgood = False

        static = is_staticfunc(f_decl)
        if(static): return False
        
        # samefile = os.path.samefile(f_decl.coord.file,self.filename)
        # if(not samefile):
            # return False
        
        # Interate ove function parameters
        for idx, param_decl in enumerate(f_decl.type.args.params):

            if(type(param_decl) == c_ast.EllipsisParam):
                ptype = "..."
                pname = ""
            else:
                ptype = self.cgen.visit(param_decl.type)
                pname = param_decl.name
            fgood = self.fgood_condition(f_decl,f_name,idx ,pname, ptype)
            if(fgood):
                break
                             
        return fgood
    
    def set_template(self,template):
        self.template_cpp = template + ".cpp"
        self.template_hpp = template + ".h"

    # Append the Method
    def append_method(self,f_decl):
        methodNode = deepcopy(f_decl)
        declaration , method = self.compose_method(methodNode)
        
        if(declaration not in self.hpp_temp):
            self.hpp_temp +=  declaration
        
        if(method not in self.cpp_temp):
            self.cpp_temp += method      
        return 
    
    # Visit each defined function in scanned file
    def visit_FuncDef(self, node):
        f_decl = node.decl
        f_name = f_decl.name
        f_good = self.func_good(f_decl)
        if(f_good):
            printv(f"{bcolors.OKGREEN}Function: " + self.cgen.visit(f_decl))
            self.append_method(f_decl) 
    
    # This method create the method for the class
    def compose_method(self,f_decl):
        
        declaration = ""
        method = ""
        
        file = open("files/templates/fbody","r")
        fbodyT = file.read()
        file.close()
        
        file = open("files/templates/fdef","r")
        fdefT = file.read()
        file.close()
            
        tDict = self.template_dictionary(f_decl)
 
        bodyTemplate = Template(fbodyT)
        defTemplate = Template(fdefT)
        
        if(tDict["defbody"] != ""):
            declaration = defTemplate.safe_substitute(tDict)
        else:
            declaration = defTemplate.safe_substitute(tDict)
            method = bodyTemplate.substitute(tDict)
        
        
        return declaration,method
    
    def method_name (self,f_name):
        
        methodname = f_name.replace(f"lv_{self.name}"," ")
        # methodname = methodname.replace(f"{self.altname}"," ")
        # methodname = methodname.replace("lv"," ")
        # methodname = methodname.replace("_"," ")
        methodname = camelCase(methodname)
        
        return methodname
    
    
    ########################################### Virtual methods implemented in derivated generator ###########################################
    
    # Check if the function scanned can be good
    def fgood_condition(self,f_decl,f_name, pidx ,pname, ptype):
        fgood = False
        
        if(pidx == 0 and 
           (self.name in f_name) and 
           (pname == self.name or pname == self.altname) and 
           (f"lv_{self.name}" in ptype or f"lv_{self.altname}" in ptype )
        ): return True
   
        return fgood
    
    def template_dictionary(self,f_decl):
                
        tDict = {
            "template" : "",
            "templatevar": "",
            "ret" : "",
            "classname" : "",
            "templateT" : "",
            "class" : "",
            "method" : "",
            "plist" : "",
            "decorations" : "",
            "before" : "",
            "fcall" : "",
            "pcall" : "",
            "after" : "",
            "defbody" : ""
            
            } 
        
        return tDict
    
    # This method create the class
    def compose_class(self):
        hppOut = None
        cppOut = None
        return hppOut,cppOut
    
    # Generate parameter list  
    def parlist(self,f_decl,params):
        list = ""
        return list
    
    #generate param call for calling C function inside cpp methods
    def parcall(self,f_decl,params):
        list = ""           
        return list
    
################################################################ END BASE GENERATOR ###########################################################








############################################################## OBJECT GENERATOR ###############################################################       
        
class CppObjGenerator(CppGenerator):
    def __init__(self):
        super().__init__()
        
    def template_dictionary(self,f_decl):
        
        f_name = f_decl.name
        ret_type = ""
        after = ""
        fcall = f_name
        
        plist = self.parlist(f_decl,f_decl.type.args.params)
        pcall = self.parcall(f_decl,f_decl.type.args.params)
        methodname = self.method_name(f_name)    
        ret = self.cgen.visit(f_decl.type.type)
                
        if("void" in ret):
            after = "return *this;"
            ret = "derivedType&"
        else: fcall = f"return {fcall}"

                 
        tDict = {
            "template" : "",
            "templatevar": "",
            "ret" : ret,
            "classname" : self.classname,
            "templateT" : "",
            "class" : "",
            "method" : methodname,
            "plist" : plist,
            "decorations" : "",
            "before" : "",
            "fcall" : fcall,
            "pcall" : pcall,
            "after" : after,
            "defbody" : ""
            
            }    
            
        if("get" in f_name):
            tDict["decorations"] = "const noexcept"
        
        return tDict
            
    def compose_class(self):
        file = open(f"files/templates/{self.template_hpp}","r")
        hpp = file.read()
        file.close()
        
        file = open(f"files/templates/{self.template_cpp}","r")
        cpp = file.read()
        file.close()
        
        hppTemplate = Template(hpp)
        cppTemplate = Template(cpp)
        
        hppOut = hppTemplate.substitute({"methods" : self.cpp_temp})
        cppOut = None

        return hppOut,cppOut
        
    
    # Generate parameter list 
    def parlist(self,f_decl,params):
        list = ""
        for idx,param in enumerate(params):
            pstring  = self.cgen.visit(param)
            if(len(params) > 1 and idx > 0):
                if idx == len(params) - 1:
                    list += f"{pstring} "
                else:
                    list += f"{pstring}, "
        return list
    
    #generate param call for calling C function inside cpp methods
    def parcall(self,f_decl,params):
        list = ""
        for idx,param in enumerate(params):
            if(type(param) == c_ast.EllipsisParam):  
                ptype = ""
                pname = "args"
            else:
                ptype = self.cgen.visit(param.type)
                pname = param.name
      
            if(idx == 0 and len(params) > 1):
                list = "cObj.get(), "
            elif(idx == 0 and len(params) == 1):
                list = "cObj.get() "
            elif idx == len(params) - 1:
                list += pname
            else:
                list += f"{pname}, "
                
        return list

        
############################################################## WIDGETS GENERATOR ##############################################################       
        
class CppWidgetsGenerator(CppGenerator):
    def __init__(self):
        super().__init__()
        
    # Generate parameter list 
    def parlist(self,f_decl,params):
        list = ""
        const = False
        if(f"lv_{self.name}_create" in f_decl.name):
            const = True
            
        for idx,param in enumerate(params):
            pstring  = self.cgen.visit(param)
            if(len(params) > 1 and idx > 0):
                if idx == len(params) - 1:
                    list += f"{pstring} "
                else:
                    list += f"{pstring}, "
            elif idx == 0 and const:
                if(len(params) > 1):
                    list += "lv_obj_t* parent, "
                else:
                    list += "lv_obj_t* parent "
        return list
    
    #generate param call for calling C function inside cpp methods
    def parcall(self,f_decl,params):
        list = ""
        const = False
        if(f"lv_{self.name}_create" in f_decl.name):
            const = True
        
        for idx,param in enumerate(params):
            if(type(param) == c_ast.EllipsisParam):  
                ptype = ""
                pname = "args..."
            else:
                ptype = self.cgen.visit(param.type)
                pname = param.name
      
            if(idx == 0 and len(params) > 1):
                if(const):
                    list = "parent ? parent : lv_scr_act(), "
                else:
                    list = "cObj.get(), "
            elif(idx == 0 and len(params) == 1):
                if(const):
                    list = "parent ? parent : lv_scr_act()"
                else:
                    list = "cObj.get()"
            elif idx == len(params) - 1:
                list += pname
            else:
                list += f"{pname}, "
                
        return list
        
    def fgood_condition(self,f_decl,f_name, pidx ,pname, ptype):
        fgood = False
        
        if(f"lv_{self.name}_create" in f_decl.name):
            return True
        
        if(pidx == 0 and 
           (self.name in f_name) and 
           (pname == self.name or pname == self.altname) and 
           (f"lv_{self.name}" in ptype or f"lv_{self.altname}" in ptype )
        ): return True
   
        return fgood
        
    def template_dictionary(self,f_decl):
    
        f_name = f_decl.name
        ret_type = ""
        after = ""
        decorations = ""
        pcall_constructor = ""
        defbody = "" 
        templatevar = "" 
        fcall = f_name
        plist = self.parlist(f_decl,f_decl.type.args.params)
        pcall = self.parcall(f_decl,f_decl.type.args.params)
        methodname = self.method_name(f_name)    
        ret = self.cgen.visit(f_decl.type.type)
        
        
        if(f"lv_{self.name}_create" in f_name):
            methodname = self.classname
            ret = ""
            decorations = f": LvBaseObj({fcall}( {pcall} ))"
            pcall = "0"
            fcall = ""
            defbody = "{ }"
        elif (is_variadicfunc(f_decl)):
            if("void" in ret):
                after = "return *this;"
                ret = "derivedType&"
                defbody = "{" + f"{fcall}( {pcall} ); {after}" + "}"
            else:
                defbody = "{" + f"return {fcall}( {pcall} ); {after}" + "}"
            plist = plist.replace("...", "ArgsT... args")
           
            templatevar = "\n\ttemplate <typename... ArgsT>"
        else:
            if("get" in f_name):
                decorations = "const noexcept"
                    
            if("void" in ret):
                after = "return *this;"
                ret = "derivedType&"
            else: fcall = f"return {fcall}"
        
        
        tDict = {
            "template" : "",
            "templatevar": templatevar,
            "ret" : ret,
            "classname" : self.classname,
            "templateT" : "",
            "class" : f"{self.classname} ::",
            "method" : methodname,
            "plist" : plist,
            "decorations" : decorations,
            "before" : "",
            "fcall" : fcall,
            "pcall" : pcall,
            "after" : after,
            "defbody" : defbody
            
            }    
            
        return tDict
        
    def compose_class(self):
        file = open(f"files/templates/{self.template_hpp}","r")
        hpp = file.read()
        file.close()
        
        file = open(f"files/templates/{self.template_cpp}","r")
        cpp = file.read()
        file.close()
        
        hppTemplate = Template(hpp)
        cppTemplate = Template(cpp)
        
        wDict = {
            "classname": self.classname,
            "uppername": f"LV{self.uppername}_H_",
            "methods": self.hpp_temp
            }
        
        hppOut = hppTemplate.substitute(wDict)
        
        wDict["methods"] = self.cpp_temp
        cppOut = cppTemplate.substitute(wDict)

        return hppOut,cppOut
        
        
############################################################## GENERIC GENERATOR ##############################################################       
        
class CppGenericGenerator(CppObjGenerator):
    def __init__(self):
        super().__init__()
        
    def template_dictionary(self,f_decl):
        
        f_name = f_decl.name
        ret_type = ""
        after = ""
        fcall = f_name
        
        plist = self.parlist(f_decl,f_decl.type.args.params)
        pcall = self.parcall(f_decl,f_decl.type.args.params)
        methodname = self.method_name(f_name)    
        ret = self.cgen.visit(f_decl.type.type)
                
        if("void" in ret):
            after = "return *this;"
            ret = f"{self.classname}&"
        else: fcall = f"return {fcall}"

                 
        tDict = {
            "template" : "",
            "templatevar": "",
            "ret" : ret,
            "classname" : self.classname,
            "templateT" : "",
            "class" : "",
            "method" : methodname,
            "plist" : plist,
            "decorations" : "",
            "before" : "",
            "fcall" : fcall,
            "pcall" : pcall,
            "after" : after,
            "defbody" : ""
            
            }    
            
        if("get" in f_name):
            tDict["decorations"] = "const noexcept"
        
        return tDict
            
    def compose_class(self):
        file = open(f"files/templates/{self.template_hpp}","r")
        hpp = file.read()
        file.close()
        
        file = open(f"files/templates/{self.template_cpp}","r")
        cpp = file.read()
        file.close()
        
        hppTemplate = Template(hpp)
        cppTemplate = Template(cpp)
        
        gDict = {
            "classname": self.classname,
            "uppername": f"LV{self.uppername}_H_",
            "methods": self.hpp_temp,
            "name" : f"lv_{self.name}_t",
            "alloc" : "lv_mem_alloc",
            "del" : "lv_free",
            "private": "",
            "objdef": ""
            }
        
        gDict["objdef"] = f"<{gDict['name']},{gDict['del']}>"
        
        hppOut = hppTemplate.substitute(gDict)
        
        
        gDict["methods"] = self.cpp_temp
        cppOut = cppTemplate.substitute(gDict)

        return hppOut,cppOut
        

        
############################################################## FIXED GENERATOR ##############################################################       
        
class CppFixedGenerator():
    def __init__(self):
        super().__init__()  
        self.filenames  = []
        
    # Scan a file
    def scan(self, filename):
        printv(f"Scanning file: {filename}")
        self.filenames.append(filename)    
        pass
     
    # Set libc path   
    def setlibc(self,libc):
        pass
    
    # Set the name of the object to generate    
    def setname(self,name):
        pass
        
    # Set the alternate name of the object to generate    
    def setalt(self,alternate):
        pass
    
    # Generate the class    
    def generate(self,opath):
        for file in self.filenames:
            shutil.copy(file,opath)
        pass
    
    def set_template(self,template):
        pass
     
        
