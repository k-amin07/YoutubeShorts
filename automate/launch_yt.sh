#!/bin/sh
# Start the youtube app
adb shell am start com.google.android.youtube

echo "starting youtube"
# su -cn u:r:system_app:s0
# add a mechanism to launch shorts and enable stats for nerds.

sleep 5
adb shell input tap 270 2200

echo "launched shorts"

sleep 1

# not sure if it is because of vanced but the shorts button is visible in the bottom bar on pixel 4 but not on pixel 6.
# Also would have to adjust the x and y coordinates in the command above based on device

# enable stats in shorts by opening the three dot menu and tapping stats for nerds

echo "opening menu"
adb shell input tap 1000 100

# this is buggy, manually tap stats for nerds because this may not always work. Only needs to be done once
sleep 1
adb shell input tap 270 2147
