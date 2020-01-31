#!/bin/bash

if [ "$(netstat -tulnap | grep -q ngrok)" ]; then
	echo found
else
	echo not found
fi

