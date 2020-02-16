#!/bin/bash

python3 ~/Script/PP-01/ngrokserverstart.py
sleep 10

gnome-terminal -- bash -c "python3 ~/Script/PP-01/bill.py; exit; exec bash"



gnome-terminal -- bash -c "python3 ~/Script/PS-01/app.py; exit; exec bash" 

echo finish...
