import ctypes  # An included library with Python install.   
import os
import zipfile
import sys
import json
import hashlib
import shutil
from functools import partial

def md5sum(filename: str):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()
args = sys.argv[1:]
if len(args) < 1:
    pass
else:
    infile = args[0]
    try:
        if os.path.isdir(infile):
            #build stuff
            pass
        elif infile.split(".")[-1] == "exz":
            cachecode = md5sum(infile)
            lfolder = os.path.expandvars(f"%TEMP%\\exz{cachecode}")
            if os.path.isdir(lfolder):
                try:
                    with open(lfolder+"\\EXZMANIFEST") as f2:
                        mdata = json.load(f2)
                except:
                    shutil.rmtree(lfolder)
                    with zipfile.ZipFile(infile) as f:
                    
                        os.mkdir(lfolder)
                        data = f.extract("EXZMANIFEST",lfolder)
                        print(data)
                        with open(data) as f2:
                            mdata = json.load(f2)
                        os.remove(data)
                        f.extractall(lfolder) 
            #Run stuff
            else:
                with zipfile.ZipFile(infile) as f:
                    
                    os.mkdir(lfolder)
                    data = f.extract("EXZMANIFEST",lfolder)
                    #print(data)
                    with open(data) as f2:
                        mdata = json.load(f2)
                    os.remove(data)
                    f.extractall(lfolder)
                
            mdata["cwd"] = os.path.expandvars(mdata["cwd"].replace(">EXTRACTDIR",lfolder))
            os.chdir(mdata["cwd"])
            if mdata["allowargs"]:
                mdata["execute"] += " " + " ".join(args[1:])#Allows args so therefore pass args to program
            e = os.system(os.path.expandvars(mdata["execute"].replace(">EXTRACTDIR",lfolder)))
            os.chdir(os.path.expandvars("%USERPROFILE%"))
            if e != 0:
                ctypes.windll.user32.MessageBoxW(0, f"Warning: Program exited with exit code {e}.\nThis may be an error.\nTo debug program data, navigate to {lfolder} and DO NOT CLOSE THIS MESSAGE BOX", "EXZ Monitor", 0)
            #shutil.rmtree(lfolder)
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"We're sorry, but a fatal error occured extracting your program.\n{str(e)}", "EXZ Error", 0)