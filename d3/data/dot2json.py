import sys
from igraph import *

# Get command line arguments
infile = sys.argv[1]
groupfiles = []
for i in range(2, len(sys.argv) ) :
	groupfiles.append( sys.argv[i] )
# don't want infile to be in groupfiles
if infile in groupfiles : groupfiles.remove( infile );

outfile = 'callgraph.json'

# Create the tree object
g = Graph(n=0,directed=True)

# Create all labelled vertices
file = open(infile,'r')
i = 0
while 1:
    line = file.readline()
    if not line:
        break
    # New vertex
    if '[' in line :
		g.add_vertices(1)
		g.vs[i]['id'] = line.split(' ')[0].strip()
		g.vs[i]['label'] = line.split('{')[1].split('}')[0]
		g.vs[i]['group'] = 0
		i = i+1
	
		 
# Add grouping information
i = 1
for groupfile in groupfiles :
	file = open(groupfile,'r')
	while 1:
		line = file.readline()
		if not line:
			break
		# Add to group i
		if '[' in line :
			label = line.split('{')[1].split('}')[0]
			v1 = g.vs.select(label_eq=label)
			if (len(v1) == 1) :
				v1[0]['group'] = i 
	i = i+1
	
# Create all edges
file = open(infile,'r')
i = 0
while 1:
    line = file.readline()
    if not line:
        break
    # New edge
    if '->' in line :
		id1 = line.split(' ')[0].strip()
		id2 = line.split(' ')[2].strip().strip(';')
		v1 = g.vs.select(id_eq=id1)
		v2 = g.vs.select(id_eq=id2)
		# Check if v2 is placeholder function
		if (len(v1)==1 & len(v2)==1) :
			g.add_edges( (v1[0].index,v2[0].index) )
			if (v1[0]['group'] == v2[0]['group']) : g.es[i]['value'] = 10
			else : g.es[i]['value'] = 1
			i = i+1
			

# Delete the 'external_node' vertex
g.delete_vertices(0)


# Traverse and print the graph as JSON
f = open(outfile,'w')
f.write( '{\n' )
f.write( '	"nodes":[\n' )

for i in range(0,len(g.vs)) :
	v = g.vs[i]
	group = v['group']
	f.write( '		{"name":"'+ v['label'] +'","group":'+ str(group) +'}' )
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



