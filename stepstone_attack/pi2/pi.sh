#!/bin/bash
if [[ $# -eq 1 ]]; then
    echo "The last attacked Pi. Done!" > debug.txt
    echo "command:" $1 >> debug.txt
    exit 0
fi

arg_array=($@)
command=${arg_array[0]}
next_stepstone=${arg_array[1]}
unset 'arg_array[1]'
next_arg_array=${arg_array[@]}

ssh pi@$next_stepstone > /dev/null 2>&1 << eeooff
    cd Workspace
    python3 publisher.py "$command"
    ./pi.sh $next_arg_array
    exit 0
eeooff

echo done!