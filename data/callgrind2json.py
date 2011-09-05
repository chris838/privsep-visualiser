#! /usr/bin/env python

import glob
import os
import time
import re
import json
import sys

# Log/output files
vg_outfile="valgrind.out"
pg_outfile="privgrind.out"
wastefile="waste.gz"

# Remove output from previous run
os.system( "rm {} {} {}".format(vg_outfile, pg_outfile, wastefile) )

"""
# Function to process dump file
def process(dump) :
	print "Processing new callgrind dump file"
"""



"""
# Create output pipe
os.system( "mkfifo {}".format(cg_outfile) )
"""

# Create valgrind/callgrind call
cg_call  = "( "
cg_call += "valgrind --tool=privgrind "
cg_call += "--log-file={} ".format(vg_outfile)
cg_call += "gzip-clanged test"
cg_call += " )"

os.system( cg_call )

"""
# Fork child process to run callgrind
pid = os.fork()
if pid :
	sys.exit()
	# Parent process - reads pipe until child is finished
	#while True :
		#os.system( 'echo "cmd:  gzip-clanged -c 5MB.zip"|cat - {} > /tmp/out; callgrind_annotate /tmp/out'.format(outfile) )
else :
	# Child process - calls valgrind to write data to the pipe
	os.system( cg_call )
	sys.exit(0)
"""
