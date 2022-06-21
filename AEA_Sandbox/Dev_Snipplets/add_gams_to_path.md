
# INSTALL GAMS THE RIGHT WAY

use this to add the GAMS to the path in the AEA Environment

example_path: `C:\GAMS\37\apifiles\Python\gams`

-----------------------------------------------------
* *leaves* VPN
* make new environment `conda create -n myNETZEROenv`
*   alternatively create env via IDE
* activate environment (conda activate myNETZEROenv
* move cursor to gams dict (see below)
* execute `setup.py install`
* everything should work now
* *enters* VPN
 -----------------------------------------------------
 
###  Alternative I
`sys.path.append(r'C:\GAMS\37\apifiles\Python\api_37')
sys.path.append(r'C:\GAMS\37\apifiles\Python\gams')
`
### Alternative II

`set PYTHONPATH=C:\GAMS\37\apifiles\Python\api_37`
`set PYTHONPATH=C:\GAMS\37\apifiles\Python\gams;%PYTHONPATH%`

