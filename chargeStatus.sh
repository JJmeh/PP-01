#!/bin/bash

tlp-stat -b | grep status | awk '{print $3}'
