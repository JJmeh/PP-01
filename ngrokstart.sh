#!/bin/bash

gnome-terminal -- bash -c "ngrok tcp $1 -region ap; exit; exec bash"
sleep 15

curl -s http://localhost:4040/api/tunnels > tunnel.json
echo $(python3 tunnels.py)
rm tunnel.json
