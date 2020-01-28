#!/bin/bash
sudo kill -9 $(ps -ef | grep temp_efficiency.py | grep -v grep | awk '{print $2}')