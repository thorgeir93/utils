#!/bin/bash

DEVICE_ID=${1}

bluetoothctl -- pair $DEVICE_ID
sleep 10
bluetoothctl -- trust $DEVICE_ID
bluetoothctl -- connect $DEVICE_ID
sleep 5
