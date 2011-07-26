var w = 900,
    h = 900,
	fill = d3.scale.category20();
	 
var vis = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);
    	

d3.json("../../data/callgraph_grouped_man.json", function(json) {
	
	// Create intra-module graphs for each module
	var arr = json.nodes;
	var subvis = new Array();
	var force = new Array();
	var link = new Array();
	var node = new Array();
	for (var i=0; i < arr.length; i++) {

		subvis[i] = vis.append("svg:g")
			.attr("class", "node");
		
		force[i] = d3.layout.force()
			.nodes(arr[i].nodes)
			.links(arr[i].links)
			.gravity(0.1)
			.distance(100)
			.charge(-100)
			.size([0, 0])
			.start();

		link[i] = subvis[i].selectAll("line.link")
			.data(arr[i].links)
			.enter().append("svg:line")
			.attr("class", "link")
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

		node[i] = subvis[i].selectAll("g.node")
			.data(arr[i].nodes)
		  .enter().append("svg:g")
			.attr("class", "node")
			.call(force[i].drag);

		node[i].append("svg:circle")
			.attr("r", function(d) { return 3+2*d.cost; } )
			.style("fill", function(d) { return fill(i); });

		node[i].append("svg:text")
			.attr("dx", 12)
			.attr("dy", ".35em")
			.text(function(d) { return d.name });

		var ticker = function(i) {
		  var i_local = i;
		  function f() {
			  link[i_local].attr("x1", function(d) { return d.source.x; })
				  .attr("y1", function(d) { return d.source.y; })
				  .attr("x2", function(d) { return d.target.x; })
				  .attr("y2", function(d) { return d.target.y; });

			  node[i_local].attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
			};
			return f;
		};
		force[i].on("tick", ticker(i) );
	
	}
	
	
	// Create inter-module graph
	var inter_force = d3.layout.force()
		.nodes(json.nodes)
		.links(json.links)
		.gravity(.05)
		.distance(300)
		.charge(-1000)
		.size([w, h])
		.start();

	var inter_node = vis.selectAll("svg > g.node")
		.data(json.nodes);

	inter_node.append("svg:text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.name });

	var f = function() {

		inter_node.attr("transform", function(d) {

			
			return "translate(" + d.x + "," + d.y + ")";
		});
	};
	inter_force.on("tick", f );
	
});
