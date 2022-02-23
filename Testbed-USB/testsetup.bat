@ECHO OFF
set "str1=Setting up testbed for motor"
set "str2=%~1"
set "str3=%str1% %str2%"
set "str4=node"
set "node=%str4% %str2%"

echo.%str3%

cd ..\..
cd

cd NXP\FreeMASTER 3.1\FreeMASTER Lite
cd

start "%node%" cmd.exe /k node.exe -b %str2%

cd ..\..\..
cd

cd testbed-usb
cd

start cmd.exe /k CALL python subscriber.py %str2%

start cmd.exe /k CALL jupyter notebook

echo "After the jupyter notebook server opens in browser, select the notebook to push variables to the motor.  Execute all lines of code in notebook, the hit return here to finish setup."

PAUSE

start cmd.exe /k CALL python testbed.py %str2%