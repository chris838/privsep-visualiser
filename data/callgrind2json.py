#! /usr/bin/env python

import glob
import os
import time
import re
import json

data_path = "updates.json"
outfile="callgrind.out"
logfile="valgrind.out"
wastefile="waste.gz"

# Hold the run of costs so far
costs = {}

# Function to process dump file
def process(dump) :
	print "Processing new callgrind dump file"
	os.system( "callgrind_annotate {}".format(outfile) )


# Remove output from previous run
os.system( "rm {} {} {}".format(outfile, logfile, wastefile) )

# Create output pipe
os.system( "mkfifo {}".format(outfile) )

# Create valgrind/callgrind call
cg_call  = "valgrind --tool=callgrind "
cg_call += "--log-file={} ".format(logfile)
cg_call += "--callgrind-out-file={} ".format(outfile)
cg_call += "--compress-pos=no "
cg_call += "--dump-every-bb=50000000 "
cg_call += "--combine-dumps=yes "
cg_call += "gzip-clanged -c 5MB.zip > {} ".format(wastefile)

# Fork child process to run callgrind
pid = os.fork()
if pid :
	# Parent process - reads pipe into callgrind_annotate until child is finished
	while True :
		os.system( 'echo "cmd:  gzip-clanged -c 5MB.zip"|cat - {} > /tmp/out; callgrind_annotate /tmp/out'.format(outfile) )
else :
	# Child process - calls valgrind to write data to the pipe
	os.system( cg_call )
	sys.exit(0)
