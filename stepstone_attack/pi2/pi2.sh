#!/bin/bash
ssh pi@10.42.0.220 > /dev/null 2>&1 << eeooff
cd Workspace
python3 publisher.py 3 "$1"
echo "$1" > test.txt
./pi3.sh "$1"
nc -zvn 10.42.0.220 1-36000
exit
eeooff
echo done!