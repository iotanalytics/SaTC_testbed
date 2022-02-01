#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo 'Usage:'
    echo './scan_attack.sh command_code ip1 ip2 ip3 ...'
    echo 'e.g. ./scan_attack.sh 192.168.0.2 192.168.0.5 192.168.0.11'
    exit 1
fi

echo $#
echo $1