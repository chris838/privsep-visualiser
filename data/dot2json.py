#! /usr/bin/env python

import sys
from igraph import *

# Get command line arguments
infiles = []
groupfiles = []
for i in range(1, len(sys.argv) ) :
	f = sys.argv[i]
	if '.dot' in f : infiles.append( f )
	if '.txt' in f : groupfiles.append( f )

# Define variables
outfile = 'd.json'
codes = ['t', 'T']

# Create the tree object
g = Graph(n=0,directed=True)

# Create all labelled vertices
i = 0
for infile in infiles :
	file = open(infile,'r')
	while 1:
		line = file.readline()
		if not line:
			break
		# New vertex
		if '[' in line :
			# Check not already present
			label = line.split('{')[1].split('}')[0].strip()
			if len(g.vs) == 0 or len(g.vs.select(label_eq=label)) == 0 :
				g.add_vertices(1)
				g.vs[i]['id'] = line.split(' ')[0].strip()
				g.vs[i]['label'] = label
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
		code = label = line.strip().split(' ')[0]
		label = label = line.strip().split(' ')[1]
		# Check if function belongs to this group
		if code in codes :
			v1 = g.vs.select(label_eq=label)
			if (len(v1) == 1) :
				v1[0]['group'] = i 
	i = i+1
	
# Create all edges
i = 0
for infile in infiles :
	file = open(infile,'r')
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
				if (v1[0]['group'] == v2[0]['group']) : g.es[i]['value'] = 1
				else : g.es[i]['value'] = 1
				g.es[i]['id'] = i
				i = i+1
		

# Delete the 'external_node' vertex
g.delete_vertices(0)

# Calculate size of groups
sizes = []
for i in range(0,len(g.vs)) :
	group = g.vs[i]['group']
	while len(sizes) <= group : sizes.append(0)
	sizes[group] += 1
	
# Calculate weights as the negated sum of end point valences
weights = [1]*len(g.es)
#for i in range(0,len(g.es)) :
#	edge = g.es[i]
#	weights[i] = -(  g.degree(g.vs[edge.source]) 
#				   + g.degree(g.vs[edge.target]) )
for i in range(0,len(g.es)) :
	edge = g.es[i]
	weights[i] = (-1) - 100*( g.vs[edge.source]['group'] == g.vs[edge.target]['group'])

# Calculate a maximum(=minimum) spanning tree
t = g.spanning_tree(weights);

# Traverse and print the graph as JSON
f = open(outfile,'w')
f.write( '{\n' )
f.write( '	"nodes":[\n' )

def write_node(f,i,degree,selected,label,area,active,visible,module,leaf,domain) :
	f.write( '		{'                  	)
	# Unique ID used to keep visualisation consistent across refresh
	f.write( '"id":'+str(i)+', '        	)
	# Node valency
	f.write( '"degree":'+str(degree)+', '	)
	# Attribute for selected nodes
	f.write( '"selected":'+str(selected)+', ')
	# Text label and size (area)
	f.write( '"label":"'+str(label)+'", '	)
	f.write( '"area":'+str(area)+', '		)
	# Overide active/visible modifiers
	f.write( '"active":'+str(active)+', '   )
	f.write( '"visible":'+str(visible)+', ' )
	# Module information
	f.write( '"module":'+str(module)+', ' 	)
	f.write( '"leaf":'+str(leaf)+', '	)
	# Domain information
	f.write( '"domain":'+str(domain)+', ' 	)
	# Cost
	f.write( '"cost":'+str(1)+' ' 	)
	f.write( '}'                        	)

def write_edge(f,i,active,visible,source,target,in_st) :
	f.write( '		{'                  	)
	# Unique ID used to keep visualisation consistent across refresh
	f.write( '"id":'+ str(i) +', '			)
	# Overide active/visible modifiers
	f.write( '"active":'+str(active)+', '   )
	f.write( '"visible":'+str(visible)+', ' )
	# Source and target nodes
	f.write( '"source":'+ str(source) +', ')
	f.write( '"target":'+ str(target) +', '	)
	# Is edge in spanning tree?
	f.write( '"in_st":'+ str(in_st) +' '	)
	f.write( '}' 							)

## Write out normal nodes
for i in range(0,len(g.vs)) :
	v = g.vs[i]
	degree = len( g.neighbors(v.index) )
	label = v['label']
	module = v['group']
	write_node(f,i,degree,0,label,1,1,1,module,1,0)
	f.write( ',')
	f.write( '\n' )
# and also nodes for each module
for i in range(0, len(groupfiles)+1) :
	degree = len( g.neighbors(v.index) )
	if i==0 : 	label = infiles[0]
	else :		label = groupfiles[i-1]
	write_node(f,i+len(g.vs),degree,0,label,sizes[i],1,0,i,0,0)
	if (i < len(groupfiles)) : f.write( ',')
	f.write( '\n' )
f.write( '	],\n' )

# Write out edges...
f.write( '	"links":[\n' )
j=0
for i in range(0,len(g.es)) :
	e = g.es[i]
	value = weights[i]
	mods = len(g.vs) + int(g.vs[e.source]['group'])
	modt = len(g.vs) + int(g.vs[e.target]['group'])
	# ...for function to function
	if len(t.es.select(id_eq=e['id']))>0 :
		# If edge is in the MST
		write_edge(f,j,1,1,e.source,e.target,1)
		j = j+1
		if (mods != modt) :
			f.write( ',\n' )
			# ...for module to function
			write_edge(f,j,1,1,mods,e.target,1)
			f.write( ',\n' )
			j = j+1
			# ...for function to module
			write_edge(f,j,1,1,e.source,modt,1)
			f.write( ',\n' )
			j = j+1
			# ...for module to module
			write_edge(f,j,1,1,mods,modt,1)
			j = j+1
	else :
		# If edge isn't in the MST
		write_edge(f,j,1,1,e.source,e.target,0)
		j = j+1
		if (mods != modt) :
			f.write( ',\n' )
			# ...for module to function
			write_edge(f,j,1,1,mods,e.target,0)
			f.write( ',\n' )
			j = j+1
			# ...for function to module
			write_edge(f,j,1,1,e.source,modt,0)
			f.write( ',\n' )
			j = j+1
			# ...for module to module
			write_edge(f,j,1,1,mods,modt,1)
			j = j+1
	if (i < len(g.es)-1) : f.write( ',')
	f.write('\n')
f.write( '	],\n' )

# Write out successors
f.write( '	"successors":[\n' )
# for each function
for i in range(0,len(g.vs)) :
	v = g.vs[i]
	f.write( '		');
	f.write( str(g.successors(v.index)) );
	if (i < len(g.vs)-1) : f.write( ',')
	f.write( '\n' )
f.write( '	]\n' )
f.write( '}' )
