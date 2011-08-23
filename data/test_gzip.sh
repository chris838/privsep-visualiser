#!/bin/bash

# Output here
outfile="dumps/callgrind.out"

# Wipe directory
rm dumps/*

# Create output pipe
mkfifo $outfile

# Run valgrind/callgrind
valgrind --tool=callgrind \
	--log-file=valgrind.out \
	--callgrind-out-file=$outfile \
	--compress-pos=no \
	--dump-every-bb=500000 \
	--combine-dumps=no \
	\
	gzip-clanged -c 5MB.zip > dumps/waste.gz
