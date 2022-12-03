import tkinter as tk
from tkinter import messagebox
import os
import zipfile
import sys
import random
import json
import shutil

args = sys.argv[1:]
if len(args) < 1:
    pass
else:
    root = tk.Tk()
    root.title("EXZ")
    root.geometry("300x100")
    mtx = tk.Label(root,text="Opening...")
    mtx.pack()
    root.update()
    root.update_idletasks()
    infile = args[0]
    try:
        if os.path.isdir(infile):
            #build stuff
            pass
        elif infile.split(".")[-1] == "exz":
            cachecode = str(random.randint(0,9999)).zfill(4)
            #Run stuff
            with zipfile.ZipFile(infile) as f:
                mtx.config(text="Reading manifest")
                root.update()
                root.update_idletasks()
                lfolder = os.path.expandvars(f"%TEMP%\\exz{cachecode}")
                os.mkdir(lfolder)
                data = f.extract("EXZMANIFEST",lfolder)
                print(data)
                with open(data) as f2:
                    mdata = json.load(f2)
                os.remove(data)
                mtx.config(text="Extracting")
                root.update()
                root.update_idletasks()
                f.extractall(lfolder)
            os.remove(data)
            mdata["cwd"] = os.path.expandvars(mdata["cwd"].replace(">EXTRACTDIR",lfolder))
            os.chdir(mdata["cwd"])
            root.withdraw()
            if mdata["allowargs"]:
                mdata["execute"] += " " + " ".join(args[1:])#Allows args so therefore pass args to program
            e = os.system(os.path.expandvars(mdata["execute"].replace(">EXTRACTDIR",lfolder)))
            os.chdir(os.path.expandvars("%USERPROFILE%"))
            if e != 0:
                messagebox.showwarning("EXZ Monitor",f"Warning: Program exited with exit code {e}.\nThis may be an error.\nTo debug program data, navigate to {lfolder} and DO NOT CLOSE THIS MESSAGE BOX")
            shutil.rmtree(lfolder)
            root.quit()
            root.destroy()
    except Exception as e:
        mtx.config(text="FATAL ERROR")
        root.update()
        root.update_idletasks()
        messagebox.showerror("EXZ",f"We're sorry, but a fatal error occured while extracting this program.\n{str(e)}")