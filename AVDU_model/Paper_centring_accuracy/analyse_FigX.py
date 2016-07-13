#!/usr/bin/python

import xml.etree.ElementTree as ET
import sml_log_parser
from subprocess import call, Popen
import os.path
import os
import time, stat, random, math
import ctypes
import struct
import csv
import numpy
from os import listdir
import matplotlib.pyplot as plt

print 'Script to generate Figure for the paper, showing centring accuracy'

wall_freqs = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8]

# the different configs
print "Running ",
print len(wall_freqs),
print " bees..."

print 'Beginning bees'
runnum = 0
baseport = 50091
running_procs = []
max_procs = 4
xml_file = "beeworldConfigCorridor.xml"

xAv = []
zAv = []
vAv = []

for i in xrange(0,4):
	if i == 0:
		# location 1, fixed wall frequency 1
		offset = -3
	if i == 1:
		# location 2, fixed wall frequency 1
		offset = 3
	if i == 2:
		# location 1, fixed wall frequency 2
		offset = -3
	if i == 3:
		# location 2, fixed wall frequency 2
		offset = 3
	for wall_freq in wall_freqs:
		runnum = runnum + 1
		print 'Getting bee ',
		print runnum
		list = [ f for f in listdir("temp{0}".format(runnum)) if f[-3:] == 'csv' ]
		list.sort()
		for l in list[-1:]:
			print l
			with open("temp{0}/{1}".format(runnum,l), 'rb') as csvfile:
				data = csv.reader(csvfile, delimiter=',', quotechar='|')
				xVals = []
				zVals = []
				vVals = []
				for row in data:
					if data.line_num != 1:
						xVals.append(-(float(row[1])+offset))
						zVals.append(float(row[3]))
						vVals.append(float(row[7]))
				xAv.append(sum(xVals[3000:])/2000)
				zAv.append(sum(zVals[3000:])/2000)
				vAv.append(sum(vVals[3000:])/2000)
print "X"
for x in xAv:
		print x
print "Z"
for z in zAv:
		print z
print "V"
for v in vAv:
		print v
		
print len(xAv[0:8])
print len(wall_freqs)
# plot
j = 0
p6xvals = []
p6xstd = []
for i in xAv[0:8]:
	p6xvals.append(numpy.mean([i, xAv[int(j+8)]]))
	p6xstd.append(numpy.std([i, xAv[int(j+8)]])/math.sqrt(2))
	j=j+1
j = 0
p15xvals = []
p15xstd = []
for i in xAv[16:24]:
	p15xvals.append(numpy.mean([i, xAv[int(j+24)]]))
	p15xstd.append(numpy.std([i, xAv[int(j+24)]])/math.sqrt(2))
	j=j+1
plt.errorbar(wall_freqs, p6xvals, yerr=p6xstd, ecolor='g')
plt.hold
plt.errorbar(wall_freqs, p15xvals, yerr=p15xstd, ecolor='r')
plt.ylim([-3,3])
plt.legend([ 'Fixed wall = 0.6 Sine','Fixed wall = 0.15 Sine'])
plt.title("Model centring accuracy")
plt.xlabel("Frequency of variable wall")
plt.ylabel("Model X location")
plt.show()
