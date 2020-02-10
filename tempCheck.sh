#!/bin/bash

tlp-stat -t | grep temp | awk '{print $4}'
