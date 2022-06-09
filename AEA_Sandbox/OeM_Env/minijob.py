import trigger_run
import generate_milestonyr_bat_include

import os
from datetime import datetime
import shutil

year_tuples = [
    (2010, 2013),
    (2010, 2014),
#    (2010, 2015),
#    (2010, 2020)
               ]

def move_run_gdx(name):
    stage = r"C:\Users\lzw\PycharmProjects\Netzero2040_Sandbox\netzero2040\AEA_Sandbox\OeM_Env\DD-Files-v02\GAMSSAVE\BASE-Model.gdx"
    storage = os.path.join(r"C:\Users\lzw\PycharmProjects\Netzero2040_Sandbox\netzero2040\AEA_Sandbox\OeM_Env\results", name)
    print(shutil.move(stage, storage))

for start, end in year_tuples:

    run_name = f"run_{start}_{end}"
    print(run_name.center(50,"~"))
    run_gdx = run_name + ".gdx"
    x = datetime.now()
    generate_milestonyr_bat_include.generate_bat_file(start=start, end=end)
    trigger_run.run()
    move_run_gdx(run_gdx)
    print("duration:", datetime.now()-x)
    print("~"*50)
    print()
