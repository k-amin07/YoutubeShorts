#!/bin/sh

mkdir -p ./data/stats/
mkdir -p ./data/screenshots/
./launch_yt.sh
sleep 2
./scroll.sh
python store_data.py