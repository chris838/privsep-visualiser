#! /usr/bin/env python

import glob
import os
import time
import re
import json

dump_path = "dumps/"
data_path = "updates.json"

# Hold the run of costs so far
costs = {}


# Function to return an array of dump files, in correct processing order
def get_dumps() :
	# Get any dump files in the dump folder
	dumps = glob.glob( dump_path+"callgrind.out.*")
	# Sort into correct order
	dumps.sort(reverse=False)
	# Make sure we get the last dump file, which is annoyingly named without
	# the numeric suffix.
	for last_out in glob.glob( dump_path+"callgrind.out") :
		dumps.append( last_out )
	return dumps


# Function to process dump file
def process(dump) :
	print "Processing new callgrind dump file"
	while 1:
		line = dump.readline()
		if not line:
			# Save out to file
			data = {"nodes":[]}
			for k in costs :
				data["nodes"].append( {"label":k, "cost":costs[k] } )
			# Use the cost to update JSON file
			data_file = open(data_path, 'w')
			data_file.write(json.dumps(data))
			data_file.close()
			break
		if re.match( '^cf[nl]=' , line) :
			funs = line.split(' ')
			if len(funs) > 1 :
				# Get the cost for this function
				fun = funs[1].strip()
				cost = 0
				dump.readline() # skip next line
				next_line = dump.readline()
				print next_line
				while re.match( '(^[\+]?\d+)|(^\*)', next_line ) :
					# sum cost over successive lines
					cost += int( next_line.split(' ')[1].strip() )
					next_line = dump.readline()
				# Update our running costs
				costs[fun] =cost + costs.get( fun, 0)
				


dumps = []
# Poll for new dump files
while True :
	
	# Get initial list of dump files
	dumps = get_dumps()
	
	# While any files left to process
	while len(dumps) > 0 :
		
		# Grab oldest unprocessed dump file
		file = dumps[0]
		
		# Process output
		process( open(file,'r') )
		
		# Remove dump file
		os.system( "rm {}".format(file) )
		
		# Update dump files list
		dumps = get_dumps()
