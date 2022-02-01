#!/bin/bash
ssh pi@10.0.0.10 >/dev/null 2>&1 << eeooff
cd /home
ls
exit
eeooff
echo done!