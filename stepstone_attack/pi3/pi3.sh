#!/bin/bash
ssh pi@10.42.0.203 > /dev/null 2>&1 << eeooff
cd Workspace
python3 publisher.py 4 "$1"
echo "$1" > test.txt
./pi4.sh "$1"
nc -zvn 10.42.0.203 1-36000
exit
eeooff
echo done!