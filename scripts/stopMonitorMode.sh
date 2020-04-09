#!/bin/bash
# this script deactivates Monitor mode on wlan1mon device

airmon-ng stop wlan1mon
ifconfig wlan1 up
ifconfig wlan0 up
