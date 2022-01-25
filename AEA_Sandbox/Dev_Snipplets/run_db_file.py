import sys

# C:\GAMS\37\apifiles\Python\gams

# -----------------------------------------------------
# -----------------------------------------------------
# INSTALL GAMS THE RIGHT WAY
# -----------------------------------------------------
# *leave* VPN
# make new environment conda create -n myNETZEROenv
#   alternatively create env via IDE
# activate environment (conda activate myNETZEROenv
# move cursor to gams dict (see below)
# execute setup.py install
# everything should work now
# *enter* VPN
# -----------------------------------------------------
import gams
import gamstransfer as gt

path = r"C:\Users\lzw\PycharmProjects\netzero2040\zwiebs_test_suite\BasicModel.gdx"
m = gt.Container()
m.read(m , path)


print(m.__dict__)