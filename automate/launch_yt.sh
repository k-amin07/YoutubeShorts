#!/bin/sh
# Start the youtube app
adb shell am start com.google.android.youtube

echo "starting youtube"

sleep 5
echo "opening shorts"
adb shell input tap 270 2200

sleep 1

tap_x=$((540 + RANDOM % 50 - 25))
tap_y=$((1100 + RANDOM % 50 - 25))
adb shell input tap $tap_x $tap_y

# not sure if it is because of vanced but the shorts button is visible in the bottom bar on pixel 4 but not on pixel 6.
# Also would have to adjust the x and y coordinates in these commands based on device

# enable stats in shorts by opening the three dot menu and tapping stats for nerds
echo "opening menu"
adb shell input tap 1000 100


sleep 1
echo "enabling stats for nerds"
adb shell input tap 270 2147
