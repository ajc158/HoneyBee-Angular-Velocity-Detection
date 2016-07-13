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

wall_freqs = [0.03, 0.12]

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

for i in xrange(0,8):
	if i < 4:
		# location 1
		offset = -3
	if i > 3:
		# location 1
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
inds = [8,10,9,11]
for i in [xAv[0],xAv[2],xAv[1],xAv[3]]:
	p6xvals.append(numpy.mean([i, xAv[int(inds[j])]]))
	p6xstd.append(numpy.std([i, xAv[int(inds[j])]])/math.sqrt(2))
	j=j+1
j = 0
p15xvals = []
p15xstd = []
inds = [12,14,13,15]
for i in [xAv[4],xAv[6],xAv[5],xAv[7]]:
	p15xvals.append(numpy.mean([i, xAv[int(inds[j])]]))
	p15xstd.append(numpy.std([i, xAv[int(inds[j])]])/math.sqrt(2))
	j=j+1
ys = [1,2,3,4]
plt.errorbar(ys, p6xvals, yerr=p6xstd, ecolor='g')
plt.hold
plt.errorbar(ys, p15xvals, yerr=p15xstd, ecolor='r')
plt.ylim([-4,4])
plt.legend([ 'Fixed wall = 0.6 Sine','Fixed wall = 0.15 Sine'])
plt.xlim([0,5])
locs = [1,2,3,4]
labels = ['Sine 0.15','Square 0.15','Sine 0.6','Square 0.6']
plt.xticks(locs,labels)
plt.title("Model centring accuracy (wide vs narrow band)")
plt.xlabel("Frequency of variable wall")
plt.ylabel("Model X location")
plt.show()
