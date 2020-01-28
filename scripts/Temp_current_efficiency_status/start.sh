#!/bin/bash
cd $1
nohup python3 status_and_features.py > start.log &