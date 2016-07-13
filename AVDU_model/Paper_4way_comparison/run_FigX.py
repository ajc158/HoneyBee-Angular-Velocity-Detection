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
Model_dir = "/Users/alex/Dropbox/Work/Papers/corridor_centre_paper/Model/Paper_4way_comparison/"

print 'Script to generate Figure for the paper, showing narrow vs wide band behaviour'

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

for i in xrange(0,8):
	if i == 0:
		# location 1, sin sin, freq 1
		xml_file = "beeworldConfigCorridorp6sinsin.xml"
		poswall = 13
		negwall = -7
	if i == 1:
		# location 1, sin square, freq 1
		xml_file = "beeworldConfigCorridorp6sinsqr.xml"
		poswall = 13
		negwall = -7
	if i == 2:
		# location 1, sin sin, freq 2
		xml_file = "beeworldConfigCorridorp15sinsin.xml"
		poswall = 13
		negwall = -7
	if i == 3:
		# location 1, sin square, freq 2
		xml_file = "beeworldConfigCorridorp15sinsqr.xml"
		poswall = 13
		negwall = -7
	if i == 4:
		# location 2, sin sin, freq 1
		xml_file = "beeworldConfigCorridorp6sinsin.xml"
		poswall = 7
		negwall = -13
	if i == 5:
		# location 2, sin square, freq 1
		xml_file = "beeworldConfigCorridorp6sinsqr.xml"
		poswall = 7
		negwall = -13
	if i == 6:
		# location 2, sin sin, freq 2
		xml_file = "beeworldConfigCorridorp15sinsin.xml"
		poswall = 7
		negwall = -13
	if i == 7:
		# location 2, sin square, freq 2
		xml_file = "beeworldConfigCorridorp15sinsqr.xml"
		poswall = 7
		negwall = -13
	for wall_freq in wall_freqs:
		runnum = runnum + 1
		print 'Running bee ',
		print runnum
	
		script_name = "batch_bee{0}.sh".format(runnum)
		fl = open(script_name, "w")
		fl.write("#!/bin/bash\n");
		fl.write("mkdir temp{0}/\n".format(runnum));
		fl.write("cp ../cc_full_model/* ./temp{0}/\n".format(runnum));
		fl.write("sed -i '' 's/50091/{0}/g' ./temp{1}/experiment4.xml\n".format(baseport+runnum,runnum));
		fl.write("cp {0} ./temp{1}/beeworldConfigCorridor.xml\n".format(xml_file,runnum));
		#fl.write("sed -i '' 's;\"./\";\"./temp{0}\";g' ./temp{0}/beeworldConfigCorridor.xml\n".format(runnum));
		fl.write("cd temp{0}\n".format(runnum));
		fl.write("../../beeworld2 ./beeworldConfigCorridor.xml {1} &\n".format(runnum, baseport+runnum))
		fl.write("sleep 2\n")
		fl.write("cd {0}\n".format(SML_2_B_dir));
		run_line = "PATH=/bin:/usr/bin:/usr/local/bin:{0}/SystemML/BRAHMS/bin/brahms/:. BRAHMS_NS={0}/SystemML/Namespace SYSTEMML_INSTALL_PATH={0}/SystemML ./convert_script_s2b -w {1} -m {2}/temp{3} -e 4 -o ./outtemp/bee{3}/".format(SML_dir, SML_2_B_dir, Model_dir,runnum)
		run_line = run_line + " -p 'changes for batch':c:{0}".format(wall_freq)
		run_line = run_line + " -p 'changes neg wall':c:{0}".format(negwall)
		run_line = run_line + " -p 'changes pos wall':c:{0}".format(poswall)
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
