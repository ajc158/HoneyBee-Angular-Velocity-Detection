#!/usr/bin/python

import xml.etree.ElementTree as ET
import sml_log_parser
from subprocess import call, Popen
import os.path
import os
import time, stat, random, math
import ctypes
import struct

SML_2_B_dir = "/Users/alex/Documents/SpineML_2_BRAHMS/"
SML_dir = "/Users/alex/bgit2/"
Model_dir = "/Users/alex/Dropbox/Work/Papers/corridor_centre_paper/Model/Paper_detector_behaviour/"

print 'Script to generate Figure for the paper, showing detector SF and contrast invariance'

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

for i in xrange(0,7):
	if i == 0:
		# SF1
		xml_file = "beeworldConfigTuning11.xml"
	if i == 1:
		# SF2
		xml_file = "beeworldConfigTuning19.xml"
	if i == 2:
		# SF3
		xml_file = "beeworldConfigTuning38.xml"
	if i == 3:
		# SF3
		xml_file = "beeworldConfigTuning76.xml"
	if i == 4:
		# SF3
		xml_file = "beeworldConfigTuningc3.xml"
	if i == 5:
		# SF3
		xml_file = "beeworldConfigTuningc4.xml"
	if i == 6:
		# SF3
		xml_file = "beeworldConfigTuningc6.xml"
	for wall_freq in wall_freqs:
		runnum = runnum + 1
		print 'Running bee ',
		print runnum
	
		script_name = "batch_bee{0}.sh".format(runnum)
		fl = open(script_name, "w")
		fl.write("#!/bin/bash\n");
		fl.write("mkdir temp{0}/\n".format(runnum));
		fl.write("cp ../cc_test_model/* ./temp{0}/\n".format(runnum));
		fl.write("sed -i '' 's/50091/{0}/g' ./temp{1}/experiment1.xml\n".format(baseport+runnum,runnum));
		fl.write("cp {0} ./temp{1}/beeworldConfigCorridor.xml\n".format(xml_file,runnum));
		fl.write("cd temp{0}\n".format(runnum));
		fl.write("../../beeworld2 ./beeworldConfigCorridor.xml {1} &\n".format(runnum, baseport+runnum))
		fl.write("sleep 2\n")
		fl.write("cd {0}\n".format(SML_2_B_dir));
		run_line = "PATH=/bin:/usr/bin:/usr/local/bin:{0}/SystemML/BRAHMS/bin/brahms/:. BRAHMS_NS={0}/SystemML/Namespace SYSTEMML_INSTALL_PATH={0}/SystemML ./convert_script_s2b -w {1} -m {2}/temp{3} -e 1 -o ./outtemp/bee{3}/".format(SML_dir, SML_2_B_dir, Model_dir,runnum)
		run_line = run_line + " -p 'changes for batch':c:{0}".format(wall_freq)
		run_line = run_line + "\n"
		fl.write(run_line);
		fl.close()
		# Now make the script executable...
		st = os.stat(script_name)
		os.chmod(script_name, st.st_mode | stat.S_IEXEC)
			
		# launch the batch, 2 batches allowed at a time
		while len(running_procs) > max_procs - 1:
			for proc in running_procs:
				retcode = proc.poll()
				if retcode is not None: # Process finished.
					running_procs.remove(proc)
		else:
			running_procs = running_procs + [Popen(['bash', script_name])]
		
# wait for remaining batches
while len(running_procs) > 0:
	for proc in running_procs:
		retcode = proc.poll()
		if retcode is not None: # Process finished.
			running_procs.remove(proc)
