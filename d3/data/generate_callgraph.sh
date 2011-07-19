#!/bin/sh

clang -emit-llvm -c $1 -o sample.o
opt -analyze -dot-callgraph sample.o
python dot2json.py callgraph.dot
