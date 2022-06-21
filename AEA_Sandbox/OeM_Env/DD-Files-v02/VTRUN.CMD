@echo off
echo Hello
Title BASE-Model [  ] [GAMS_WRKTIMES]
CALL ..\GAMS_SRCTIMESV454\VT_GAMS BASE-Model GAMS_SRCTIMESV454 GAMSSAVE\BASE-Model
::rem GDX2VEDA GAMSSAVE\BASE-Model ..\GAMS_SRCTIMESV454\times2veda.vdd BASE-Model
echo Closed >RunTerminated
::C:\VEDA\VEDA_FE\ResultDBMaker.exe C:\VEDA\VEDA_FE\GAMS_WRKTIMES\BASE-Model.VD

echo process_finished
