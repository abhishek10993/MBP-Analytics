#!/bin/bash
sudo kill -9 $(ps -ef | grep electricity_usage.py | grep -v grep | awk '{print $2}')