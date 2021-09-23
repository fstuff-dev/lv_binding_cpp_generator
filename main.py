'''
@author: fstuff-dev
'''

from mainutils import *
from generators import *

# Main Script
if __name__ == '__main__':
    
    # Start Application
    print("# Generating LVGL C++ Binding #")
    
       
    # Get Parameters
    lvgl,binding,verb,confpath = scan_arg(sys.argv)
    setverbose(verb)
    
    if(lvgl):   
        # Load Config
        confall = load_config(confpath)
        confall["globals"]["ipath"] = lvgl
        confall["globals"]["opath"] = binding
        
        configurations = confall["configurations"]
        
        try:
            # Try to generate
            if("configurations" in confall):
                for config in configurations:
                    generate(config,confall["globals"])
            # End Application
            print(f"# Binding '{confall[globals]['bindingname']}' Generated #")
        except Exception as e:
            print("# End #")


    


    
    

    

            
            