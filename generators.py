'''
Created on Jun 30, 2021

@author: fstuffdev
'''

import sys
import os
import shutil
import re
from work.cppstylegen import CppStyeGenerator
sys.path.extend(['.', '..'])
from work.cppwidgetgen import CppWidgetGenerator, generateWidgetsHeader
from work.cppgenericgen  import CppGenericGenerator
from work.cpptimergen  import CppTimerGenerator
from work.cpptimelinegen import CppTimelineGenerator
from work.cppanimgen import CppAnimGenerator



def getGenerator(wname):
    
    if(wname == "style"):
        return CppStyeGenerator()
    
    if(wname == "timer"):
        return CppTimerGenerator()
    
    if(wname == "anim"):
        return CppAnimGenerator()
    
    if(wname == "anim_timeline"):
        return CppTimelineGenerator()
    
    
    return CppGenericGenerator()

        
def lvwidget(inpath,extrapath,outpath, wname):
    
    automaticscan = False
    gen = CppWidgetGenerator()
    gen.setStdLibPath(r'utils/fake_libc_include')
    
    if(not wname):
        automaticscan = True
    else:
        gen.setName(wname)
        
    fileScan = os.listdir(inpath)
    if(wname == "include"):
        generateWidgetsHeader(inpath)
    else:
        for file in fileScan:
            fname = inpath + file
            file_name, file_extension = os.path.splitext(fname)
            
            if("lv_"  in file and file_extension == ".c"):
                
                pattern = r'lv_(.*).c'
                try:
                    substr = re.match(pattern, file).group(1)
                except AttributeError:
                    substr = ''
                if(automaticscan):
                    wname = substr
                    
                gen.setName(wname)
                gen.scan(fname)
                if(wname != "obj"):
                    gen.generate(outpath)
                    
                   
        if(wname == "obj"):
            flex_path = os.path.join(extrapath,"layouts/flex")
            grid_path = os.path.join(extrapath,"layouts/grid")
            gen.scan(flex_path + "/lv_flex.c")
            gen.scan(grid_path + "/lv_grid.c")
            gen.generate(outpath)

def lvGeneric(inpath,extrapath,outpath, wname, altname):
    
    gen = getGenerator(wname)
    gen.setAltname(altname)
    gen.setStdLibPath(r'utils/fake_libc_include')
    
    fileScan = os.listdir(inpath)
    for file in fileScan:
        fname = inpath + file
        file_name, file_extension = os.path.splitext(fname)
        if("lv_"  in file and file_extension == ".c"):     
            pattern = r'lv_(.*).c'
            try:
                substr = re.match(pattern, file).group(1)
                if(wname in substr):
                    gen.setName(wname)
                    gen.scan(fname)
                    
            except AttributeError:
                substr = None
                break
            
    if(wname == "style"):
        flex_path = os.path.join(extrapath,"layouts/flex")
        grid_path = os.path.join(extrapath,"layouts/grid")
        gen.scan(flex_path + "/lv_flex.c")
        gen.scan(grid_path + "/lv_grid.c")
             
    gen.generate(outpath)
            
def libSkeleton(inpath, opath,copy = False):
    if(not os.path.exists(opath)): 
        os.mkdir(opath)
    else:
        shutil.rmtree(opath)
        os.mkdir(opath)
        
    #Copy the input lib folder skeleton
    if(copy):
        for t in os.walk(inpath):
            relpath = os.path.relpath(t[0], inpath)
            realOutPath = os.path.join(opath, relpath)
            if(relpath != "."):
                os.mkdir(realOutPath)
            print(realOutPath)
    else:
        srcpath = os.path.join(opath, "src/")
        corepath = os.path.join(opath, "src/core/")
        widgetspath = os.path.join(opath, "src/widgets/")
        os.mkdir(srcpath)
        os.mkdir(corepath)
        os.mkdir(widgetspath)
        for t in os.walk(opath):
            print(t[0])
    pass

    
def lvcore(inpath, outpath):
    pass
