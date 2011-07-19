from igraph import *

# Create the tree object
g = Graph(directed=True)


# Create all labelled vertices
file = open('callgraph.dot','r')
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
		i = i+1
		
# Create all edges, and unlabelled vertices
file = open('callgraph.dot','r')
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
		# Both v1 and v2 should have one item in
		if (len(v1) == 1 & len(v2)==1) :
			g.add_edges( (v1[0].index,v2[0].index) )
		 
print summary(g)

# Traverse and print the graph as JSON
def traverse(f,g,v):
  next = g.successors(v)
  if len( next )==0 :
	  f.write( '{"name" : "'+ g.vs[v]['label'] +'", "size" : 2000 }\n' )
  else :
	  f.write( '{' )
	  f.write( '"name" : "'+ g.vs[v]['label'] +'",\n' )
	  f.write( '"children" : [\n' )
	  
	  # print first one
	  traverse(f,g,next[0])
	  
	  # print any more, after a comma
	  for i in range(1,len(next)) :
		  f.write( ',\n' )
		  traverse(f,g,next[i])
	  
	  f.write( ']\n' )
	  f.write( '}\n' )


f = open('callgraph_tree.json','w')
traverse(f,g,0)



