#!/bin/sh
COUNTER=1

while true
do
  # UI Automator does not grab the screen content unless the screen is static. We need to pause the video for this. Its an old abandoned library but it lets us control any app
  adb shell input tap 540 1100
  echo "dumping stats"
  adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
  adb shell input tap 540 1100
  echo "\n\n" >> ./stats/$COUNTER.xml
  sleep 15
  adb shell input tap 540 1100
  adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
  adb shell input tap 540 1100
  echo "\n\n" >> ./stats/$COUNTER.xml
  sleep 15
  adb shell input tap 540 1100
  adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
  adb shell input tap 540 1100
  echo "\n\n" >> ./stats/$COUNTER.xml
  sleep 15
  adb shell input tap 540 1100
  adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
  adb shell input tap 540 1100
  echo "\n\n" >> ./stats/$COUNTER.xml
  echo "swiping up"
  # Swipe to next short - the command takes x-start, y-start, x-end, y-end and the time taken to execute the swipe. We can slow it down but 100ms is fine
  adb shell input touchscreen swipe 500 2000 500 1000 100
done
