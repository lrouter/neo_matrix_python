#!/bin/bash

#modprobe adxl34x
#modprobe adxl34x-i2c

#test for 1 hour. If the dedicated folder is missing, return error.
testResult="fail"
startSecond=$(date +%s)
while :
do
	file=$(find /sys/bus/i2c/drivers/adx34x -name "postion")
	if [ ! -n "$file" ]; then
		echo "Error. There is no position file."
		break
	fi
	
	endSeconds=$(date +%s)
	cost=$(( ${endSecond}-${startSecond} ))
	if [ ${cost} -gt 3600 ]; then
		testResult="success"
		break
	fi
done

echo "Test ${testResult}"


