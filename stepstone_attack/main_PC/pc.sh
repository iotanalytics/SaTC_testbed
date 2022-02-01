#!/bin/bash
ssh pi@10.42.0.187 > /dev/null 2>&1 << eeooff
echo connected
exit
eeooff
echo done!