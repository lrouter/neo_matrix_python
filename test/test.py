#!/usr/bin/python

import os
import time
import neo_matrix_python as neo

neo.board_init
sp = neo.Speaker()
count = 0
while count < 10:
	sp.setMusicNum(count)
	sp.getPlayStat()
	count = count + 1	


