#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo 'Usage:'
    echo './scan_attack.sh command_code ip1 ip2 ip3 ...'
    echo 'Example:'
    echo './scan_attack.sh 5 192.168.0.2 192.168.0.5 192.168.0.11'
    echo 'If no ip addresses given, default attack will be launched.'
    exit 1
fi

# Default attack mode.
if [[ $# -eq 1 ]]; then
    echo 'Default attack without specific ip addresses...'
    ssh pi@10.42.0.187 > /dev/null 2>&1 << eeooff
    cd Workspace
    echo "$1" > test.txt
    python publisher.py "$1"
    ./pi1.sh "$1" 
    nc -zvn 10.42.0.187 1-36000
    exit
eeooff
exit 0
fi

arg_array=($@)
command=${arg_array[0]}
next_stepstone=${arg_array[1]}
echo 'next_stepstone:' $next_stepstone
unset 'arg_array[1]'
next_arg_array=${arg_array[@]}
echo "next arguments: "$next_arg_array
echo "command:" $command
ssh pi@$next_stepstone > /dev/null 2>&1 << eeooff
    cd Workspace
    nc -zvn $next_stepstone 1-36000
    python3 publisher.py "$command"
    stress --cpu 16 --io 4 --vm 2 --vm-bytes 128M --timeout 20s
    ./pi.sh $next_arg_array
    exit 0
eeooff

echo done!
exit 0
