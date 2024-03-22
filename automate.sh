#!/bin/sh

mkdir -p ./data/stats/
mkdir -p ./data/screenshots/
mkdir -p ./data/processed/
./automate/launch_yt.sh
sleep 2
./automate/scroll.sh
