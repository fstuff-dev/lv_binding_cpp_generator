'''
Created on Sep 4, 2021

@author: fstuffdev
'''

import sys
import os
from virtualenv.config.convert import NoneType
sys.path.extend(['.', '..'])

from pycparser import c_ast, c_generator, parse_file
from pycparser.c_ast import FuncDecl
from miscutil.mutil import camelCase
from work.typ import typeMatch 


#Base class for generating Cpp methods
class CppGenerator(c_ast.NodeVisitor):
    
    def __init__(self):
        self.fake_lib_path = ""
        self.name = ""
        self.enable_dbg = False
        self.capName = ""
        self.hppFilename = "_hpp"
        self.cppFilename = "_cpp"
        self.template = ""
        self.altname = "obj"

    def setStdLibPath(self, path):
        self.fake_lib_path = path
    
    def setName(self, name):
        self.name = name
        self.objName = self.name.replace("_"," ").title().replace(" ","")
        
        self.capName = "Lv" + self.objName
        self.hppFilename = self.capName + "_hpp"
        self.cppFilename = self.capName + "_cpp"
        
    def setAltname(self, name):
        self.altname = name

    def scan(self, filename):
        ast = parse_file(filename,
                              use_cpp=True,
                              cpp_path='gcc',
                              cpp_args=['-nostdinc', '-E' , '-DPYCPARSER' ,'-I' + self.fake_lib_path]
                              )
        self.visit(ast)

    def debug(self):
        self.enable_dbg = True
        
    def gen_cppfunc_name(self, f_decl):
        pass   
    
    def cpp_func(self):
        return ""
    
    def hpp_func(self):
        return ""
    
    def  fgood_check_condition(self,f_decl,f_name, pidx ,pname, ptype):
        return False
    
    def func_good(self, f_decl):
        generator = c_generator.CGenerator()
        f_name = f_decl.name
        fgood = False
        
        if(self.is_staticfunc(f_decl)):
            return False
        
        # Scan functions and look for good function
        for idx, param_decl in enumerate(f_decl.type.args.params):
            if(type(param_decl) == c_ast.EllipsisParam):
                ptype = "..."
                pname = ""
            else:
                ptype = generator.visit(param_decl.type)
                pname = param_decl.name
            
            fgood = self.fgood_check_condition(f_decl,f_name,idx ,pname, ptype)
            if(fgood):
                break
            
        print("Function {0} good: {1}".format(f_name,fgood))
            
                         
        return fgood
    
    def write_function(self, hppString, cppString):
        present = False
        if(os.path.exists(self.hppFilename)):
            hppFileTemp = open(self.hppFilename, "r")
            hppTemp = hppFileTemp.read()
            present = hppString in hppTemp    
            hppFileTemp.close()

        # Write if not present    
        if(not present):
            hppFileTemp = open(self.hppFilename, "a")
            cppFileTemp = open(self.cppFilename, "a")    
            hppFileTemp.write("\n\t" + hppString)
            cppFileTemp.write("\n" + cppString)
            hppFileTemp.close()
            cppFileTemp.close()
            
    def new_type(self,type_node,itype):
        if(type(type_node) == c_ast.PtrDecl):
            if(type(type_node.type) == c_ast.PtrDecl):
                type_node.type.type.type.clear()
                type_node.type.type.type.names.append(itype)
            else:
                type_node.type.type.names.clear()
                type_node.type.type.names.append(itype)
        else:
            type_node.names.clear()
            type_node.names.append(itype)
        return
            
    def func_par(self, f_decl):
        fcall_par = ""
        generator = c_generator.CGenerator()
            
        for idx, param_decl in enumerate(f_decl.type.args.params):
            if(type(param_decl) == c_ast.EllipsisParam):  # i don't know how to generate ellipsis parameters
                ptype = ""
                pname = "args"
            else:
                ptype = generator.visit(param_decl.type)
                
                newtype = typeMatch(ptype)
                if(newtype):
                    self.new_type(param_decl.type,newtype)
                    pname = param_decl.name + "->raw()"
                else:
                    pname = param_decl.name
                
            if  self.enable_dbg:
                print("Arg: ", ptype, pname)
                    
            if(idx == 0 and len(f_decl.type.args.params) > 1):
                fcall_par = "cObj.get(),"
            elif(idx == 0 and len(f_decl.type.args.params) == 1):
                fcall_par = "cObj.get()"
            elif idx == len(f_decl.type.args.params) - 1:
                fcall_par += pname
            else:
                fcall_par += pname + ","
                
        return fcall_par
    
    def is_chainable(self, f_name):
        chain_crit = {"setStyle", "addStyle", "setCol", "setRow"}
        res = True
        return res
    
    def is_variadicfunc(self, f_decl):
        
        if(type(f_decl.type.args) != NoneType):
            for idx, param_decl in enumerate(f_decl.type.args.params):
                if(type(param_decl) == c_ast.EllipsisParam): 
                    return True
                else:
                    pass
        return False
    
    def is_staticfunc(self, f_decl):

        if(len(f_decl.storage) > 0 and f_decl.storage[0] == "static"):
            if(len(f_decl.funcspec) > 0 and f_decl.funcspec[0] == "inline"):
                return False 
            else: 
                return True
        return False
    
    def fdef_gen(self, f_decl, f_call):
        
    # /*FTEMPLATE*/
    # /*FCALL*/
        
        template = "" 
               
        fdef_file = open("templates/FDef_T", "r")
        fdef_t = fdef_file.read()
        
        if(self.is_variadicfunc(f_decl)):
            template = "template <typename... ArgsT>\n"
        
        fdef_mod = fdef_t.replace("/*FTEMPLATE*/", template)
        fdef_mod = fdef_mod.replace("/*FCALL*/", f_call)
        
        fdef_file.close()
            
        return fdef_mod
    
    def fbody_gen(self, f_decl):
        
        generator = c_generator.CGenerator()
        f_name = f_decl.name
        fcall_par = self.func_par(f_decl)
        ret_type = generator.visit(f_decl.type.type)
        
    # /*FDECORATIONS*/
    # /*FBEFORE*/
    # /*FCALL*/
    # /*FAFTER*/
    # /*FRET*/
    # /*FCPP*/
        
        decorations = "" 
        before = ""
        call = ""
        after = ""
        ret = ""
        cpp = ""
        
        fbody_file = open("templates/Fbody_T", "r")
        fbody_t = fbody_file.read()
        
        call = f_name + "(" + fcall_par + ");"
        
        if(ret_type == "void"):
            ret = "return *this;"
            f_decl.type.type.type.names[0] = self.capName + "&"
        else:
            call = "return " + call
            
        if(("get" in f_name) and not (ret_type == "void")):
            decorations = " const noexcept "
         
        # fbody_mod = fbody_t.replace("/*FCPP*/",cpp)
        # fbody_mod = fbody_mod.replace("/*FDECORATIONS*/",decorations)
        
        fbody_mod = fbody_t.replace("/*FDECORATIONS*/", decorations)
        fbody_mod = fbody_mod.replace("/*FBEFORE*/", before)
        fbody_mod = fbody_mod.replace("/*FCALL*/", call)
        fbody_mod = fbody_mod.replace("/*FAFTER*/", after)
        fbody_mod = fbody_mod.replace("/*FRET*/", ret)
        
        fbody_file.close()
        
        return fbody_mod  
    
    def flush_cppmember(self, cppMember, cppFuncName):
        if(type(cppMember.type.type) == c_ast.PtrDecl):
            if(type(cppMember.type.type.type) == c_ast.PtrDecl):
                cppMember.type.type.type.type.declname = cppFuncName
            else:
                cppMember.type.type.type.declname = cppFuncName
        else:
            cppMember.type.type.declname = cppFuncName
    
        if(len(cppMember.type.args.params) > 0 and cppMember.type.args.params[0]):
            del cppMember.type.args.params[0]
    
        if(len(cppMember.funcspec) > 0 and cppMember.funcspec[0] == "inline"):
            del cppMember.funcspec[0]
        if(len(cppMember.storage) > 0 and cppMember.storage[0] == "static"):
            del cppMember.storage[0] 
            
        return cppMember 
    
    def flush_hppmember(self, cppMember, fname_mod):
             
        if(type(cppMember.type.type) == c_ast.PtrDecl):
            if(type(cppMember.type.type.type) == c_ast.PtrDecl):
                cppMember.type.type.type.type.declname = fname_mod
            else:
                cppMember.type.type.type.declname = fname_mod
        else:
            cppMember.type.type.declname = fname_mod   
            
        return cppMember 
   
    def visit_FuncDef(self, node):
                # create a C file genrator
        generator = c_generator.CGenerator()
        f_decl = node.decl
        f_name = f_decl.name
        variadicFunc = False
        ret_type = generator.visit(f_decl.type.type)
      
        # Scan functions and look for good function
        fgood = self.func_good(f_decl)
        variadicFunc = self.is_variadicfunc(f_decl)
        
        # The function is good
        if(fgood):
    
            if  self.enable_dbg:
                print("")
                # node.show()
                print("\n\rDef ->", generator.visit(f_decl))
                print("Defined at: ", f_decl.coord)
                print ("Ret: ", ret_type)
                print ("Function: ", f_name)
                      
            # Modify function to cppMember
            fname_mod = f_name.replace("lv_" + self.name, '')
            fname_mod = camelCase(fname_mod)
            fname_mod = fname_mod.replace('_', '')   
            
            fbody_mod = self.fbody_gen(f_decl)
            fdef_mod = self.fdef_gen(f_decl, fname_mod)
            
            cppFuncName = "{0}::{1}".format(self.capName, fname_mod)
            self.flush_cppmember(f_decl, cppFuncName)
            
            # cpp
            if(not variadicFunc):
                cppString = generator.visit(f_decl) + fbody_mod
            else:
                cppString = ''
            
            # hpp
            self.flush_hppmember(f_decl, fname_mod)
            if(variadicFunc):
                hppString = "\n\ttemplate <typename... ArgsT>\n\t" + generator.visit(f_decl).replace("...", "ArgsT... args") + fbody_mod.replace("args", "args...") + ";"
            else:
                if(("get" in generator.visit(f_decl)) and not(ret_type == "void")):
                    hppString = generator.visit(f_decl) + " const noexcept " + ";"
                else:
                    hppString = generator.visit(f_decl) + ";"
              
            print(hppString)
            #
            # Check if function is already present in file
            self.write_function(hppString, cppString)
    
    def set_template_fname(self, template_fname=None):
        if(template_fname):
            self.template = template_fname

    def template_replace_cpp(self, cpp, cppMeth):
        return ""
    
    def template_replace_hpp(self, hpp, hppMeth):
        return ""
                 
    def generate(self, outpath):
        
        print("")
        print("Generating " + self.capName + " from Template")
             
        self.set_template_fname()

        # open and read files
        
        if(not(os.path.exists(self.hppFilename) and os.path.exists(self.cppFilename))):
            file = open(self.hppFilename, "w")
            file.close()
            
            file = open(self.cppFilename, "w")
            file.close()
        
        classCpp = open(self.template + ".cpp", "r")
        classHpp = open(self.template + ".h", "r")
        
        hppTemp = open(self.hppFilename)
        cppTemp = open(self.cppFilename)
            
        cpp = classCpp.read()
        hpp = classHpp.read()
        cppMeth = cppTemp.read()
        hppMeth = hppTemp.read()
        
        cpp = self.template_replace_cpp(cpp, cppMeth)
        hpp = self.template_replace_hpp(hpp, hppMeth)
                   
        cppOut = open(outpath + self.capName + ".cpp", "w")
        cppOut.write(cpp)
        
        hppOut = open(outpath + self.capName + ".h", "w")
        hppOut.write(hpp)
        
        classHpp.close()
        classCpp.close()
        hppTemp.close()
        cppTemp.close()
        
        cppOut.close()
        hppOut.close()
        
        os.remove(self.hppFilename)
        os.remove(self.cppFilename)
        
        pass
    
