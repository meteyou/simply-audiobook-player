#!/bin/bash

CURRENT_PID=`pgrep -f "python simply-audiobook-player.py"`
if [ -n "${CURRENT_PID}" ]; then
    echo "There is already Simply-Audiobook-Player running with PID:$CURRENT_PID"
    exit
fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $CURRENT_DIR
python simply-audiobook-player.py &
