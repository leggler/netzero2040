import subprocess
import os
import glob

def run():
    dd_dir = "DD-Files-v02"
    save_folder = os.path.join(dd_dir,"GAMSSAVE")
    os.makedirs(save_folder, exist_ok=True)
    os.chdir(dd_dir)
    for file in glob.glob(save_folder+"\\*.gdx"):
        print(os.remove(file))


    # todo clean up VT_GAMS übernehmen
    cmd = r"C:\GAMS\win64\24.2\gams.exe BASE-Model.RUN IDIR=..\\GAMS_SRCTIMESV454 GDX=GAMSSAVE\BASE-Model"
    print(cmd)
    print(subprocess.run(cmd))
    os.chdir("..")
