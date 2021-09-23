'''
@author: fstuff-dev
'''

from re import sub
from pycparser import c_ast


# function to convert string to camelCase
def camelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]

# Verbose mode
verb = False
def printv(str):
    global verb
    if(verb):
        print(str + bcolors.ENDC)
        
def setverbose(v):
    global verb
    verb = v
        
# Color for console    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




################################################################# PYCPARSER ####################################################################  

# Check if a function is variadic
def is_variadicfunc( f_decl):
    if(not f_decl.type.args):
        for idx, param_decl in enumerate(f_decl.type.args.params):
            if(type(param_decl) == c_ast.EllipsisParam): 
                return True
            else:
                pass
    return False
    
# Check if a function is a static method
def is_staticfunc( f_decl):
    if(len(f_decl.storage) > 0 and f_decl.storage[0] == "static"):
        if(len(f_decl.funcspec) > 0 and f_decl.funcspec[0] == "inline"):
            return False 
        else: 
            return True
    return False

# Remove or change a parameter value in a list
def remove_func_par_at(params, idx = 0, newvalue = None):
    
    if(idx < params.len()):
        if(newvalue):
            params[idx] = newvalue
        else:
            del params[idx]
            

            
    
    
    
    
    
    
    
    
 
