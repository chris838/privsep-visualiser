import sys
import re
from igraph import *

# Get command line arguments
infile = sys.argv[1]
outfile = 'callgraph.twopi.json'

# Create the tree object
g = Graph(n=0,directed=True)


# Create all labelled vertices
file = open(infile,'r')
i = j = 0
while 1:
	# Check end of file
	line = file.readline()
	if not line:
		break
	if re.search("Node0x[0-9a-f ]*->[ ]*Node0x[0-9a-f ]*\[", line, re.I):
		# New edge
		id1 = line.split(' ')[0].strip()
		id2 = line.split(' ')[2].strip().strip(';')
		v1 = g.vs.select(id_eq=id1)
		v2 = g.vs.select(id_eq=id2)
		# Check if v2 is placeholder function
		if (len(v1)==1 & len(v2)==1) :
			g.add_edges( (v1[0].index,v2[0].index) )
			g.es[j]['value'] = 1
			j = j+1
	elif re.search("Node0x[0-9a-f ]*\[", line, re.I):
		# New vertex
		props = line.split('[')[1].split(']')[0].split(',')
		if len(props) > 5 :
			g.add_vertices(1)
			g.vs[i]['id'] = line.split(' ')[0].strip()
			g.vs[i]['label'] = props[0].split('{')[1].split('}')[0]
			g.vs[i]['x'] = props[2].split('"')[1].strip()
			g.vs[i]['y'] = props[3].strip('"').strip()
			i = i+1

# Delete the 'external_node' vertex
g.delete_vertices(0)


# Traverse and print the graph as JSON
f = open(outfile,'w')
f.write( '{\n' )
f.write( '	"nodes":[\n' )

for i in range(0,len(g.vs)) :
	v = g.vs[i]
	group = 0
	f.write( '		')
	f.write( '{"name":"'+ v['label'] )
	f.write( '","group":'+ str(group) )
	f.write( ', "x":'+v['x']+', "y":'+v['y']+'}' )
	if (i < len(g.vs)-1) : f.write( ',')
	f.write( '\n' )
f.write( '	],\n' )

f.write( '	"links":[\n' )
for i in range(0,len(g.es)) :
	e = g.es[i]
	value = e['value']
	f.write( '		{"source":'+ str(e.source) +',"target":'+ str(e.target) +',"value":'+str(value)+'}' )
	if (i < len(g.es)-1) : f.write( ',')
	f.write( '\n' )
f.write( '	]\n' )
f.write( '}' )
