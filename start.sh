#!/bin/bash

script_dir=$(dirname "$(realpath "$0")")
cd "$script_dir"

# Find any running main.py processes and kill them if found
main_pid=$(ps aux | grep '[p]ython main.py' | awk '{print $2}')
if [ ! -z "$main_pid" ]; then
    echo "Found a running main.py process, process ID: $main_pid"
    kill $main_pid
    echo "Killed the main.py process"
fi

# Start a new main.py process and redirect input and output to nohup.out
nohup .venv/bin/python main.py > nohup.out 2>&1 &

echo "Started a new main.py process"

