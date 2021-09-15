'''
Created on Aug 9, 2021

@author: fstuffdev
'''

import os
import sys
import generators

outlibname = "lv_binding_cpp"

if __name__ == '__main__':
    
    if(len(sys.argv) <= 2 ):
        sys.exit(-1)
        
    lvglpath = sys.argv[1] 
    lvglppath = sys.argv[2]
    lvglppRealPath = os.path.join(lvglppath,outlibname)   
    
    # <rel_path,wname>
    widgetsGenArgs = (("src/core/","obj"),
                    ("src/widgets/",None),
                    ("src/extra/widgets/animimg/",None),
                    ("src/extra/widgets/calendar/","calendar"),
                    ("src/extra/widgets/chart/",None),
                    ("src/extra/widgets/colorwheel/",None),
                    ("src/extra/widgets/imgbtn/",None),
                    ("src/extra/widgets/keyboard/",None),
                    ("src/extra/widgets/led/",None),
                    ("src/extra/widgets/list/",None),
                    ("src/extra/widgets/meter/",None),
                    ("src/extra/widgets/msgbox/",None),
                    # ("src/extra/widgets/span/",None),
                    ("src/extra/widgets/spinbox/",None),
                    ("src/extra/widgets/spinner/",None),
                    ("src/extra/widgets/tabview/",None),
                    # ("src/extra/widgets/titleview/",None),
                    ("src/extra/widgets/win/",None)
                      )
    
      # <rel_path,wname,alternate_wname>
    GenericArgs = (("src/misc/","style",""),
                   ("src/misc/","timer",""),
                   ("src/misc/","anim","a"),
                   ("src/misc/","anim_timeline","at"),
                   (None,None))

    try:
        #Generating lib skeleton
        generators.libSkeleton(lvglpath,lvglppRealPath,True)
        
        
        #Generating Generics
        for GenericArg in GenericArgs:
            if(GenericArg[0]):
                extra = os.path.join(lvglpath,"src/extra")
                opath = os.path.join(lvglppRealPath,GenericArg[0])
                ipath = os.path.join(lvglpath,GenericArg[0])
                generators.lvGeneric(ipath, extra,opath,GenericArg[1],GenericArg[2])
        
        #Generating widgets
        for widgetArg in widgetsGenArgs:
            ipath = os.path.join(lvglpath,widgetArg[0])
            extra = os.path.join(lvglpath,"src/extra")
            if(widgetArg[1] != "obj"):
                opath = os.path.join(lvglppRealPath,"src/widgets/")
            else:
                opath = os.path.join(lvglppRealPath,"src/core/")
            generators.lvwidget(ipath, extra,opath, widgetArg[1])
            
        opath = os.path.join(lvglppRealPath,"src/widgets/")
        generators.lvwidget(opath,"",None,"include")
        
        
    except OSError:
        print("Generation Error")
        sys.exit()
        
    print("\n" + outlibname +" Generated !!!")
    
    pass