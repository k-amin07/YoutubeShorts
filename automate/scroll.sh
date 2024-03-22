#!/bin/sh
COUNTER=1

## There would be buffering time for 2G, this works fine on wifi, would have to adjust for 2G.
intermittent_wait=14

while true
do
  mkdir -p ./data/stats/${COUNTER}
  mkdir -p ./data/screenshots/${COUNTER}
  for i in {1..4}
  do
    tap_x=$((540 + RANDOM % 50 - 25))
    tap_y=$((1100 + RANDOM % 50 - 25))

    tap_x2=$((540 + RANDOM % 50 - 25))
    tap_y2=$((1100 + RANDOM % 50 - 25))

    echo "pausing shorts"
    adb shell input tap $tap_x $tap_y
    sleep 2
    echo "dumping stats"
    adb exec-out uiautomator dump /dev/tty >> ./data/stats/${COUNTER}/${i}.xml
    adb exec-out screencap -p > ./data/screenshots/${COUNTER}/${i}.png
    echo "resuming shorts"
    adb shell input tap $tap_x2 $tap_y2
    
    sleep $intermittent_wait
  done
  swipe_x_start=$((500 + RANDOM % 50 - 25))
  swipe_y_start=$((2000 + RANDOM % 50 - 25))
  swipe_x_end=$((500 + RANDOM % 50 - 25))
  swipe_y_end=$((1000 + RANDOM % 50 - 25))
  duration=$((RANDOM % 100 + 40))
  echo "swiping up"
  echo "\n*************"
  # Swipe to next short with slight diagonal movement
  adb shell input touchscreen swipe $swipe_x_start $swipe_y_start $swipe_x_end $swipe_y_end $duration
  sleep 1

  ## Launch the python script to parse the current short data in the background
  cd automate
  python store_data.py -p $COUNTER &
  cd ..
  # Increment counter
  ((COUNTER++))
done
