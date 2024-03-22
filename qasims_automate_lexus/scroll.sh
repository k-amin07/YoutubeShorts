#!/bin/sh
COUNTER=1

## There would be buffering time for 2G, this works fine on wifi, would have to adjust for 2G.
intermittent_wait=5
#14

# for j in {1..3}
  # do
  for i in {1..2}
  do
    tap_x=$((400 + RANDOM % 50 - 25))
    tap_y=$((550 + RANDOM % 50 - 25))

    tap_x2=$((400 + RANDOM % 50 - 25))
    tap_y2=$((550 + RANDOM % 50 - 25))

    adb shell input tap $tap_x $tap_y
    echo "dumping stats"
    sleep 2
    adb exec-out uiautomator dump /dev/tty >> ./data/stats/${COUNTER}_${i}.xml
    IMAGE_NAME="${COUNTER}_${i}"
    adb exec-out screencap -p > ./data/screenshots/$IMAGE_NAME.png
    adb shell input tap $tap_x2 $tap_y2
    echo -e "\n\n" >> ./data/stats/${COUNTER}_${i}.xml
    sleep $intermittent_wait
  done
  swipe_x_start=$((400 + RANDOM % 50 - 25))
  swipe_y_start=$((500 + RANDOM % 50 - 25))
  swipe_x_end=$((400 + RANDOM % 50 - 25))
  swipe_y_end=$((300 + RANDOM % 50 - 25))
  duration=$((RANDOM % 100 + 40))
  echo "swiping up"
  # Swipe to next short with slight diagonal movement
  adb shell input touchscreen swipe $swipe_x_start $swipe_y_start $swipe_x_end $swipe_y_end $duration
  sleep 1
  # Increment counter
  ((COUNTER++))
  # done
