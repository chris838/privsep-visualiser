// Global vars
var w = 900,
    h = 900,
    scale = 1.5,
	fill = d3.scale.category20();
				
	
// SVG container element
var svg = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);

// Bind elements to JSON data
d3.json("../../data/callgraph.twopi.json", function(json) {
	
	// Force, just to calculate edges from JSON
	var force = self.force = d3.layout.force()
			.nodes(json.nodes)
			.links(json.links)
			.start()
			.stop();
	
	// Edges
	var link = svg.selectAll("line.link")
			.data(json.links)
		.enter().append("svg:line")
			.attr("class", "link")
			.attr("style","fill:none;stroke:grey;stroke-width:1")
			.attr("x1", function(d) {return scale*d.source.x;})
			.attr("y1", function(d) {return scale*d.source.y;})
			.attr("x2", function(d) {return scale*d.target.x;})
			.attr("y2", function(d) {return scale*d.target.y;});
			
	// Vertices
	var node = svg.selectAll("g.node")w
		.data(json.nodes)
	  .enter().append("svg:g")
		.attr("class", "node")
		.attr("transform", function(d) { return "translate(" + scale*d.x + "," + scale*d.y + ")"; });
		
	node.append("svg:circle")
		.attr("r", 5)
		.style("fill", function(d) { return fill(d.group); });
		
	node.append("svg:text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.name });
		
});
