#!/bin/bash

./sshstartup.sh
sleep 10

gnome-terminal -- bash -c "python3 bill.py; exit; exec bash"
sleep 5

echo finish...
