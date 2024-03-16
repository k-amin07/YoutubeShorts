#!/bin/sh

mkdir -p ./stats
./automate/launch_yt.sh
sleep 2
./automate/scroll.sh

# COUNTER=1
#
#
#
# # Start the youtube app
# adb shell am start com.google.android.youtube
#
# echo "starting youtube"
# # su -cn u:r:system_app:s0
# # add a mechanism to launch shorts and enable stats for nerds.
#
# sleep 5
# adb shell input tap 270 2200
#
# echo "launched shorts"
#
# sleep 3
#
# # not sure if it is because of vanced but the shorts button is visible in the bottom bar on pixel 4 but not on pixel 6.
# # Also would have to adjust the x and y coordinates in the command above based on device
#
# # enable stats in shorts by opening the three dot menu and tapping stats for nerds
#
# echo "opening menu"
# adb shell input tap 1000 100
#
# # this is buggy, manually tap stats for nerds because this may not always work. Only needs to be done once
# sleep 1
# adb shell input tap 270 2147
#
# ##
# ## For some weird reason, the part above works fine if the while loop is disabled, but doesnt work correctly if the while loop is enabled
# ##
#
# # while true
# # do
# #   # UI Automator does not grab the screen content unless the screen is static. We need to pause the video for this. Its an old abandoned library but it lets us control any app
# #   adb shell input tap 540 1100
# #   echo "dumping stats"
# #   adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
# #   adb shell input tap 540 1100
# #   echo "\n\n" >> ./stats/$COUNTER.xml
# #   sleep 15
# #   adb shell input tap 540 1100
# #   adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
# #   adb shell input tap 540 1100
# #   echo "\n\n" >> ./stats/$COUNTER.xml
# #   sleep 15
# #   adb shell input tap 540 1100
# #   adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.xml
# #   adb shell input tap 540 1100
# #   echo "\n\n" >> ./stats/$COUNTER.xml
# #   sleep 15
# #   adb shell input tap 540 1100
# #   adb exec-out uiautomator dump /dev/tty >> ./stats/$COUNTER.txt
# #   adb shell input tap 540 1100
# #   echo "\n\n" >> ./stats/$COUNTER.xml
# #   echo "swiping up"
# #   # Swipe to next short - the command takes x-start, y-start, x-end, y-end and the time taken to execute the swipe. We can slow it down but 100ms is fine
# #   adb shell input touchscreen swipe 500 2000 500 1000 100
# # done
