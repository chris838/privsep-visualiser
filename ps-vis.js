var w = 900,
    h = 900,
    scale = 3,
    distance = 20,
    charge = -30,
    gravity = 0.1,
    friction = 0.9,
	fill = d3.scale.category20();

var force = d3.layout.force()
				.size([w, h]);

var data,
	nodes_filtered,
	links_filtered;
	
var svg = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);
    
var layer_links = svg.append('svg:g');
var layer_nodes = svg.append('svg:g');

d3.json("data/d.json", function(json) {
	// Store data so we can update later
	data = json;
	update();
});
	
function update() {
	
	// Define the filtered data, without non-active nodes
	nodes_filtered = data.nodes.filter(function(d) {return d.active;});
	links_filtered = data.links.filter(function(d) {
		if (isNumber(d.source)) d.source = data.nodes[d.source];
		if (isNumber(d.target)) d.target = data.nodes[d.target];
		if (d.active && d.source.active && d.target.active) {
				return true;
		} else return false;		
	});
	links_filtered2 = data.links.filter(function(d) {
		if (isNumber(d.source)) d.source = data.nodes[d.source];
		if (isNumber(d.target)) d.target = data.nodes[d.target];
		if (d.source.active && d.target.active) {
				return true;
		} else return false;		
	});


	// Bind edges
	var link = layer_links.selectAll("g.link")
			.data(links_filtered2,function(d) {return d.id;});
			
	var line = link.enter().append("svg:g")
			.attr("class", "link")
		.append("svg:line")
			.attr("style","fill:none;stroke:grey;stroke-width:1")
			.attr("x1", function(d) {return d.source.x;} )
			.attr("y1", function(d) {return d.source.y;} )
			.attr("x2", function(d) {return d.target.x;} )
			.attr("y2", function(d) {return d.target.y;} );
			
	// Exit any old edges.
	link.exit().remove();
	
	
	// Bind nodes
	var node = layer_nodes.selectAll("g.node")
		.data(nodes_filtered,function(d) {return d.id;});
		
	var contain = node.enter().append("svg:g")
			.attr("class", function(d) {return "node group" + d.group;})
			.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
			.on("click", click)
			.call(force.drag);

	contain.append("svg:circle")
		.attr("r", function(d) { d.r = 4*Math.sqrt(d.area); return d.r;})
		.style("fill", function(d) { return fill(d.group); });

	contain.append("svg:text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.label });
		
	// Exit any old nodes.
	node.exit().remove();
	
	// Update force layout
	force
		.nodes(nodes_filtered,function(d) {return d.id;})
		.links(links_filtered,function(d) {return d.id;})
		.distance( function(d) {
			return ( scale*(distance + d.source.r + d.target.r) );
		})
		.charge(charge*scale)
		.friction(friction)
		.gravity(gravity)
		.start();

	// Define tick force function
	force.on("tick", function() {
	  contain.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	
	  line.attr("x1", function(d) {return d.source.x;} )
		.attr("y1", function(d) {return d.source.y;} )
		.attr("x2", function(d) {return d.target.x;} )
		.attr("y2", function(d) {return d.target.y;} );
	});
	
	// Define drag function
	//force.drag

}

// Toggle children on click.
function click(d) {
	
	
	if (!d.m) {
		// If a function node
		for (var i=0; i < data.nodes.length; i++) {
			if (data.nodes[i].group == d.group) {
				// Show module
				if (data.nodes[i].m) data.nodes[i].active = true;
				// Hide all group functions
				else 				 data.nodes[i].active = false;
			}
		}
	} else {
		// Or if a module node
		// Show all group functions
		/*
		for (var i=0; i < data.nodes.length; i++) {
			if (data.nodes[i].group == d.group)
				data.nodes[i].active = true;
		}
		*/
		// Hide module
		d.active = false;
	}

	// Rebind to data and redraw
	update();
	
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
