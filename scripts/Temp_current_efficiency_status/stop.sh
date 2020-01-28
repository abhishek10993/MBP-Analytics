#!/bin/bash
sudo kill -9 $(ps -ef | grep status_and_features.py | grep -v grep | awk '{print $2}')