#!/bin/bash

# 

# Run valgrind/callgrind
privgrind --log-file=data.json gzip-clanged *.bin && gunzip *.gz
