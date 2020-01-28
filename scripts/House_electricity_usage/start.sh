#!/bin/bash
cd $1
nohup python3 electricity_usage.py > start.log &