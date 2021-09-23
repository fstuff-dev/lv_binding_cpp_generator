'''
@author: fstuff-dev
'''
import os
import sys
import json
from pycparser import c_ast, c_generator, parse_file
from pycparser.c_ast import FuncDecl
from util import *

# Print the application Help
def print_help():
    print("\nParameters:")
    print("-h\t Print this help")
    print("-i\t Set lvgl input folder\t\t- default: lvgl")
    print("-o\t Set binding output folder\t- default: .")
    print("-c\t Set Config file\t\t- default: config.json")
    print("-v\t Set verbose mode\t\t- default: disabled")
    return

# Scan the input arguments
def scan_arg(arg):
    iterator = iter(arg)
    ipath = "./lvgl"
    opath = "."
    confpath = "config.json"
    verbose = False
    
    # Iterating over arguments   
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break 
        else:    
            # Print Help
            if(item == "-h"):
                print_help()
                return None,None,None,None
                break  
            # Set input lvgl relative path
            if(item == "-i"):
                ipath = next(iterator)
            # Set binding relative path
            if(item == "-o"):
                opath = next(iterator) 
            # Set config file 
            if(item == "-c"):
                confpath = next(iterator) 
            # Enable verbose mode
            if(item == "-v"):
                verbose = True  

    return ipath,opath,verbose,confpath

# Load the configuration from file
def load_config(file):
    # Load config from file
    confJeson = open(file,"r")
    confPython = json.load(confJeson)
    confJeson.close()
    
    # Print basic information
    printv(f"Binding\t:{confPython['globals']['version']}")
    printv(f"Lvgl\t:{confPython['globals']['version_lvgl']}")
    printv(f"Name\t:{confPython['globals']['bindingname']}")
    
    return confPython
















