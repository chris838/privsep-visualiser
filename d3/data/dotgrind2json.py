import sys
from igraph import *

# Get command line arguments
infile = sys.argv[1]
grindfile = sys.argv[2]


outfile = "callgrindgraph.json"

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
		g.vs[i]['count'] = 0
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
			i = i+1
			
# Colour edges according to callgrind input
file = open(grindfile,'r')
while 1:
    line = file.readline()
    if not line:
        break
    # New edge
    if 'cfn=' in line :
		if len(line.split(' ')) > 1 :
			# Extract function name
			fun = line.split(' ')[1].strip()
			# Extract call count
			line = file.readline()
			count = line.split('=')[1].split(' ')[0].strip()
			# Check if matching node exists and increase count
			node = g.vs.select(label_eq=fun) 
			if len(node)==1 :
				old_count = node[0]['count']
				node[0]['count'] = int(count) + int(old_count)


# Delete the 'external_node' vertex
g.delete_vertices(0)


# Traverse and print the graph as JSON
f = open(outfile,'w')
f.write( '{\n' )
f.write( '	"nodes":[\n' )

for i in range(0,len(g.vs)) :
	v = g.vs[i]
	group = 1
	count = v['count']
	f.write( '		{"name":"'+ v['label'] +'","group":'+ str(group) +',"count":'+ str(count) +'}' )
	if (i < len(g.vs)-1) : f.write( ',')
	f.write( '\n' )
f.write( '	],\n' )

f.write( '	"links":[\n' )
for i in range(0,len(g.es)) :
	e = g.es[i]
	value = 1
	f.write( '		{"source":'+ str(e.source) +',"target":'+ str(e.target) +',"value":'+str(value)+'}' )
	if (i < len(g.es)-1) : f.write( ',')
	f.write( '\n' )
f.write( '	]\n' )
f.write( '}' )



