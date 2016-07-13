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

SML_2_B_dir = "/Users/alex/Documents/SpineML_2_BRAHMS/"

wall_freqs = [10, 
	12.5892541179, 
	15.8489319246, 
	19.9526231497, 
	25.1188643151, 
	31.6227766017, 
	39.8107170553, 
	50.1187233627,
	63.095734448,
	79.4328234724,
	100,
	125.8925411794,
	158.4893192461,
	199.5262314969,
	251.188643151,
	316.2277660168,
	398.1071705535,
	501.1872336273,
	630.9573444802,
	794.3282347243,
	1000]

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

vals = []

for i in xrange(0,7):
	for wall_freq in wall_freqs:
		runnum = runnum + 1
		print 'Getting bee ',
		print runnum
		log_dir = "{0}/outtemp/bee{1}/log/".format(SML_2_B_dir, runnum)
		log = sml_log_parser.sml_log(log_dir, 'av_out_logrep.xml')
		data = log.getdataforindex(0)
		#print len(data)
		a = numpy.array(data)
		vals.append(a[-1])
print "Vals"
for val in vals:
		print val


# plot
p1 = plt.plot(wall_freqs, vals[0:21],'r')
plt.hold
p2 = plt.plot(wall_freqs, vals[21:42],'g')
p3 = plt.plot(wall_freqs, vals[42:63],'b')
p4 = plt.plot(wall_freqs, vals[63:84],'y')
plt.legend(['11Hz','19Hz','38Hz','76Hz'])
#plt.ylim([-3,3])
#plt.xlim([0,5])
plt.xscale('log')
plt.title("Spatial frequency invariance")
plt.xlabel("Angular velocity (deg/s)")
plt.ylabel("Detector response")

plt.figure()
p2 = plt.plot(wall_freqs, vals[84:105],'g')
plt.hold
p3 = plt.plot(wall_freqs, vals[105:126],'b')
p4 = plt.plot(wall_freqs, vals[126:147],'y')
p1 = plt.plot(wall_freqs, vals[21:42],'r')
plt.legend(['2:3','2:4','2:6','2:8'])
plt.xscale('log')
plt.title("Contrast invariance")
plt.xlabel("Angular velocity (deg/s)")
plt.ylabel("Detector response")

plt.show()
