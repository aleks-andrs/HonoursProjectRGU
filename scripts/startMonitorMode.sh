#!/bin/bash
# this script enables the monitor mode on wlan1 network device

ifconfig wlan0 down
airmon-ng start wlan1



