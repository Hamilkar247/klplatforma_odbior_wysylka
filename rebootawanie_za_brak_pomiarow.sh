#!/bin/bash

number=$(cat /run/user/1000/reset_portu_usb.py.error | wc -l)
if [ "$number" -gt 10 ]; then
    sudo reboot
else
    echo "bledy sa ale jeszcze nie resetuje"
fi

