#!/bin/bash
ssh pi@10.42.0.187 > /dev/null 2>&1 << eeooff
cd Workspace
echo "$1" > test.txt
python publisher.py 1 "$1"
./pi1.sh "$1"
nc -zvn 10.42.0.187 1-36000
exit
eeooff
echo done!