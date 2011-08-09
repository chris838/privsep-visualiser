var w = 900,
    h = 900,
	padding = 0;
   
var min_cost = 1,
	num_domains = 0;
   
var scale = 3,
    distance = 20,
    charge = -50,
    gravity = 0.05,
    friction = 0.9,
	fill = d3.scale.category20();
	
var click_point = [0,0];

var force = d3.layout.force()
				.size([w, h]);

var data,
	lookup = new Array(),
	nodes_filtered,
	links_filtered;
	
var svg = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);
var frame = svg.append("svg:rect")
    .attr("width", w)
    .attr("height", h)
	.style("fill", "none")
	.style("stroke", "#aaa")
	.style("stroke-width", 1.5)
	.attr("pointer-events", "all")
	.on("mousedown", mousedown);
    
var layer_links = svg.append('svg:g');
var layer_nodes = svg.append('svg:g');


// Load data and attach update event
d3.json("data/d.json", function(json) {
	// Store data so we can update later
	data = json;
	// Create lookup table of node labels
	for (var i=0; i < data.nodes.length; i++ ) {
		lookup[ data.nodes[i].label ] = data.nodes[i]
	}
	// Run update canvas function
	update();
});

// Update canvas	
function update() {
	
	// Define filtered data sets, for visible and active (i.e. layout
	// contributing) nodes and edges.
	nodes_visible = data.nodes.filter(function(d) {
		var visible = 	d.visible &&
						(d.cost >= min_cost);
		return visible;
	});
	links_active = data.links.filter(function(d) {
		if (isNumber(d.source)) d.source = data.nodes[d.source];
		if (isNumber(d.target)) d.target = data.nodes[d.target];
		var active = 	d.in_st &&
						//(d.source.leaf == d.target.leaf) &&
						(d.source.cost >= min_cost) &&
						(d.target.cost >= min_cost) &&
						(d.source.domain == d.target.domain) &&
						d.source.visible && d.target.visible;
		return active;		
	});
	links_visible = data.links.filter(function(d) {
		if (isNumber(d.source)) d.source = data.nodes[d.source];
		if (isNumber(d.target)) d.target = data.nodes[d.target];
		if (d.source.visible && d.target.visible &&
						(d.source.cost >= min_cost) &&
						(d.target.cost >= min_cost)
		) {
				return true;
		} else return false;		
	});


	// Draw edges
	var link = layer_links.selectAll("g.link")
			.data(links_visible,function(d) {return d.id;});
			
	var line = link.enter().append("svg:g")
			.attr("class", "link")
		.append("svg:line")
			.attr("x1", function(d) {return d.source.x;} )
			.attr("y1", function(d) {return d.source.y;} )
			.attr("x2", function(d) {return d.target.x;} )
			.attr("y2", function(d) {return d.target.y;} );
	
	// Redraw edges
	layer_links.selectAll("line")
		.transition()
			.duration(0)
			.attr("style",function(d)
			{
							width = (1+2*d.in_st);
							col ="rgb(190,190,190)";
				return "fill:none;stroke:"+col+";stroke-width:"+width;
			});
			
	// Exit any old edges.
	link.exit().remove();
	
	
	// Draw nodes
	var node = layer_nodes.selectAll("g.node")
		.data(nodes_visible,function(d) {return d.id;});
		
	var contain = node.enter().append("svg:g")
			.attr("class", "node")
			.attr("transform",
				function(d) {
					return "translate(" + d.x + "," + d.y + ")";
				})
			.on("click", module_click)
			.call(force.drag);

	contain.append("svg:circle")
		.attr("r", function(d) {
			d.r = 4*Math.sqrt(d.area); return d.r;
			//d.r = 1 || Math.log( d.cost );
			return d.r;
		})
		.style("fill", function(d) {return fill(d.module); })
		.style("stroke", function(d) {
				if (d.selected) return "black";
				return "white";
			})
		.style("stroke-width", "2");
		
			
	// Redraw circle nodes
	layer_nodes.selectAll("circle")
		.transition()
			.duration(0)
			.attr("r", function(d) {
				d.r = 4*Math.sqrt(d.area); return d.r;
				//d.r = 1 || Math.log( d.cost );
				return d.r;
			});
	
	contain.append("svg:text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.label });
		
	// Exit any old nodes.
	node.exit().transition()
		.duration(0)
		.style("opacity", 0)
		.remove();
	
	// Update force layout
	force
		.nodes(nodes_visible,function(d) {return d.id;})
		.links(links_active,function(d) {return d.id;})
		.distance( function(d) {
			return ( scale*(distance + d.source.r + d.target.r) );
		})
		.charge( scale*charge )
		.friction(friction)
		.gravity(gravity)
		.start();
		
	

	// Define tick force function
	force.on("tick", function(e) {
		
	  contain.attr("transform", function(d) { 
		  return "translate(" + d.x + "," + d.y + ")"; });
	
	  line.attr("x1", function(d) {return d.source.x;} )
		.attr("y1", function(d) {return d.source.y;} )
		.attr("x2", function(d) {return d.target.x;} )
		.attr("y2", function(d) {return d.target.y;} );
		
		// Push nodes toward their designated focus.
		if (num_domains > 0) {
			var k = 2 * e.alpha;
			nodes_visible.forEach(function(o) {
				o.x += o.domain==1 ? k : -k;
			});
		}
	});
	

}

// Click handler to expand and collapse nodes
function module_click(d) {
	
	click_point = [this.x, this.y];
	
	// Select and the remove to redraw
	/*
	d.selected=1;
	var parent = this.parentNode;
	parent.removeChild(this);
	*/

	if (d.leaf) {
		// If a function node
		for (var i=0; i < data.nodes.length; i++) {
			if (data.nodes[i].module == d.module) {
				// Show module
				if (!data.nodes[i].leaf) data.nodes[i].visible = true;
				// Hide all group functions
				else 				 data.nodes[i].visible = false;
			}
		}
	} else {
		// Or if a module node
		// Show all group functions
		
		for (var i=0; i < data.nodes.length; i++) {
			if (data.nodes[i].module == d.module)
				data.nodes[i].visible = true;
		}
		
		// Hide module
		d.visible = false;
	}

	
	// Rebind to data and redraw
	update();
	
}


// Button event handlers

// Refresh data from JSON file
function refresh() {
	
	// Set min_cost to be displayed
	min_cost = 2;
	
	// Load any updates data and attach update event
	d3.json("data/updates.json", function(json) {
		
		// Node updates
		for (var i in json.nodes) {
			var node = json.nodes[i];
			var node_update = lookup[ node.label ]
			if (node_update != undefined) {
				node_update.area = Math.log( node.cost );
				node_update.cost = Math.log( node.cost );  
			}
		}
	
		// Run update canvas function
		update();
		
	});
	
}
// Split selected nodes into domain
function split() {

	// Set selected to new domain
	for (var i=0; i < data.nodes.length; i++) {
		if (data.nodes[i].selected) data.nodes[i].domain = 1;
	}
	
	num_domains = 1; 
	
	// Rebind to data and redraw
	update();
}
// Unstick fixed nodes
function unstick() {
	// Set selected to new domain
	for (var i=0; i < data.nodes.length; i++) {
		data.nodes[i].fixed = 0;
	}
	// Rebind to data and redraw
	update();
}


// Mouse event handlers for selecting nodes
var rect, x0, x1, count;
var   minx,
	  maxx,
	  miny,
	  maxy;
function mousedown() {
	x0 = d3.svg.mouse(this);

	rect = d3.select(this.parentNode)
	.append("svg:rect")
	  .style("fill", "#999")
	  .style("fill-opacity", .5);

	d3.event.preventDefault();
}
function mousemove() {
	if (!rect) return;
	x1 = d3.svg.mouse(rect.node());

	minx = Math.min(x0[0], x1[0]);
	maxx = Math.max(x0[0], x1[0]);
	miny = Math.min(x0[1], x1[1]);
	maxy = Math.max(x0[1], x1[1]);

	rect
	  .attr("x", minx - .5)
	  .attr("y", miny - .5)
	  .attr("width", maxx - minx + 1)
	  .attr("height", maxy - miny + 1);
}
function mouseup() {
	if (!rect) return;
	rect.remove();
	rect = null;
	/*
	// Grab nodes with the rectangle
	layer_nodes.selectAll("g.node")
		.attr("selected", function(d) {
			d.selected = d.selected || (minx <= d.x && maxx >= d.x
				&&  miny <= d.y && maxy >= d.y);
			return d.selected;
		})
	layer_nodes.selectAll("circle")
		.style("stroke", function(d) {
			if (d.selected) return "black";
			return "white";
		});
	*/
}
// Attach to window
d3.select(window)
	.on("mousemove", mousemove)
	.on("mouseup", mouseup);

// Helper function to check if number
function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
