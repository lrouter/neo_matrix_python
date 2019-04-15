#!/bin/bash

cp -f ${1}/drivers/* /lib/modules/$(uname -r)/drivers/input/misc/
depmod