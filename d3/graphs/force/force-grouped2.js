var w = 900,
    h = 900,
    scale =2,
	fill = d3.scale.category20();
	
var vis = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("../../data/callgraph_grouped.json", function(json) {
	
	var force = self.force = d3.layout.force()
				.nodes(json.nodes)
				.links(json.links)
				.gravity(.05)
				.distance(50)
				.charge(-500)
				.size([w, h])
				.start();

	var link = vis.selectAll("g.link")
			.data(json.links)
		.enter().append("svg:g")
			.attr("class", "link");
		
	var line = link.append("svg:line")
			.attr("style","fill:none;stroke:grey;stroke-width:1")
			.attr("x1", function(d) {return d.source.x;} )
			.attr("y1", function(d) {return d.source.y;} )
			.attr("x2", function(d) {return d.target.x;} )
			.attr("y2", function(d) {return d.target.y;} );

	var node = vis.selectAll("g.node")
		.data(json.nodes)
	  .enter().append("svg:g")
		.attr("class", "node")
		.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
		.on("click", click)
		.call(force.drag);

	node.append("svg:circle")
		.attr("r", 5)
		.style("fill", function(d) { return fill(d.group); });

	node.append("svg:text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.name });

	force.on("tick", function() {
	  node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	
	  line.attr("x1", function(d) {return d.source.x;} )
		.attr("y1", function(d) {return d.source.y;} )
		.attr("x2", function(d) {return d.target.x;} )
		.attr("y2", function(d) {return d.target.y;} );
	});

});

// Toggle children on click.
function click(d) {
  console.log(d);
}
