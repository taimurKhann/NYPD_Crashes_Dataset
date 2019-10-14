#!/bin/sh

service nginx start

nohup mongod &

python main.py

python stations.py

python index.py
