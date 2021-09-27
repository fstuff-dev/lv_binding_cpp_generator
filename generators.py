'''
Created on Jun 30, 2021

@author: fstuffdev
'''

import sys
import os
import shutil
from util import *
from cpp import *
from string import Template


# Get generator class
def get_generator(arg):
    if("generator" in arg):
        
        printv(f"\n{bcolors.WARNING}### Using : {arg['generator']} generator for {arg['name']}")
        
        if(arg["generator"] == "obj"):
            return CppObjGenerator()
        
        if(arg["generator"] == "widgets"):
            return CppWidgetsGenerator()
        
        if(arg["generator"] == "generic"):
            return CppGenericGenerator()
        
        if(arg["generator"] == "fixed"):
            return CppFixedGenerator()
        
    return CppGenerator()


def get_files(arg,absipath):
    
    file_list = []
    
    #Auto scan
    if("autoscan" in arg and arg["autoscan"]):
        dir = os.path.join(absipath,arg["relpath"])
        fileScan = os.listdir(dir)
        
        for file in fileScan:
            fname = os.path.join(dir,file) 
            file_name, file_extension = os.path.splitext(fname)
            if(f"lv_{arg['name']}"  in file_name and file_extension == ".c"):
                file_list.append(fname)
    else:
        #files to scan
        if("filetoscan" in arg):
            for file in arg["filetoscan"]:
                if("relpath" in arg):
                    f = os.path.join(absipath,file)
                else:
                    f = os.path.join(arg["path"],file)
                file_list.append( f )
    
    #offtree files to scan
    if("offtree" in arg):
        for file in arg["offtree"]:
            file_list.append( os.path.join(absipath,file) )
            
            
    printv(f"\nFile to scan for {arg['name']}") 
    for file in file_list:
        printv(file)
    
    return file_list




# Check if output path exist and flush it
def flushopath(opath):
    if(os.path.exists(opath)): 
        shutil.rmtree(opath)    
    os.mkdir(opath)
    
# Generate skeleton        
def skeleton(skel,confglobals):
    absopath = os.path.join(confglobals["opath"],confglobals["bindingname"])
    printv("\n# Building skeleton #")
    flushopath(absopath)
    for relpath in skel["paths"]:
        abspath = os.path.join(absopath,relpath)
        os.mkdir(abspath)
        printv(f"Dir: {abspath}")
        






# Simple generator
def simplegen(args,confglobals):
    
    absopath = os.path.join(confglobals["opath"],confglobals["bindingname"])
    absipath = confglobals["ipath"]
    libc = confglobals["libcpath"]
    
    
    # Generate for each argument in configuration
    for arg in args:
        files = get_files(arg,absipath)
        classopath = os.path.join(absopath,arg["relopath"])
        gen = get_generator(arg)
        
        # If Generator is implemented run generation
        if(gen):
            gen.setlibc(libc)
            gen.setname(arg["name"])
            gen.set_template(arg["template"])
            
            if("altname" in arg):
                gen.setalt(arg["altname"])
            
            for file in files:    
                gen.scan(file)
            gen.generate(classopath)
 
# Generate binding generic
def generics(args,confglobals):
    printv("\n# Building generics #")
    simplegen(args,confglobals)
    pass

# Generate binding widgets
def widgets(args,confglobals):
    printv("\n# Building widgets #")
    simplegen(args,confglobals)
    pass

# Generate fixed binding class
def fixed(args,confglobals):
    printv("\n# Building fixed #")
    simplegen(args,confglobals)
    pass

# Generate widgets header
def widgetsHeader(confglobals):
    printv("\n# Building Widgets header #")
    absopath = os.path.join(confglobals["opath"],confglobals["bindingname"],"src/widgets")
    includes = ""
    
    ext = ('.h')
    for file in os.listdir(absopath):
        if file.endswith(ext):
            includes += f'\n#include "{file}"'
        else:
            continue
    
    templateFile = open("files/templates/LvWidgets.h","r")
    templateHeader = Template(templateFile.read())
    templateFile.close()
    
    outfile = templateHeader.substitute({"includes":includes})
    
    fname = os.path.join(absopath,"LvWidgets.h")
    file = open(fname,"w")
    file.write(outfile)
    file.close()
    
    pass







# Generate the binding
def generate(conf,confglobals):
       
    # Generat only if opath and bindingname exist
    if("opath" in confglobals and "bindingname" in confglobals ):

        # Generate Skeleton
        if("skeleton" in conf):
            skeleton(conf["skeleton"],confglobals)
            
        # Generate Generic
        if("generic" in conf):  
            generics(conf["generic"],confglobals)
            
        # Generate Widgets
        if("widgets" in conf):    
            widgets(conf["widgets"],confglobals)
        
        # Generate Widgets Header   
        widgetsHeader(confglobals)
            
        # Generate Fixed class
        if("fixed" in conf): 
            fixed(conf["fixed"],confglobals)
    pass








