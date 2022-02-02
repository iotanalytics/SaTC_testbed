#!/bin/bash
ssh pi@10.42.0.189 > /dev/null 2>&1 << eeooff
cd Workspace
python3 publisher.py "$1"
echo "$1" > test.txt
./pi2.sh "$1"
nc -zvn 10.42.0.189 1-36000
exit
eeooff
echo done!