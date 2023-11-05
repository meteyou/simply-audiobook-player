#!/bin/bash
CURRENT_PID=`pgrep -f "/home/pi/simply-audiobook-player-env/bin/python simply-audiobook-player.py"`
if [ -n "${CURRENT_PID}" ]; then
    kill -SIGINT $CURRENT_PID
else
    echo "simply-audiobook-player is not running."
fi
