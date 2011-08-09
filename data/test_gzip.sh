#!/bin/sh

rm dumps/*;

valgrind --tool=callgrind \
	--log-file=valgrind.out \
	--callgrind-out-file=dumps/callgrind.out \
	--dump-every-bb=50000000 \
	--combine-dumps=no \
	\
	gzip-clanged -c 200MB.zip > dumps/waste.gz &
