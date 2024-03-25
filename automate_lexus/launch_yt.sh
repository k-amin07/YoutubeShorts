#!/bin/sh
# Start the youtube app
adb shell am start com.google.android.youtube

echo "starting youtube"

sleep 8
echo "opening shorts"
adb shell input tap 270 1750

sleep 1

tap_x=$((540 + RANDOM % 50 - 25))
tap_y=$((600 + RANDOM % 50 - 25))
adb shell input tap $tap_x $tap_y


# Also would have to adjust the x and y coordinates in these commands based on device

# enable stats in shorts by opening the three dot menu and tapping stats for nerds
echo "opening menu"
adb shell input tap 1000 100


sleep 1
echo "enabling stats for nerds"
adb shell input tap 270 1650
adb shell input tap $tap_x $tap_y
