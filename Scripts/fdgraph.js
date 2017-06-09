/**
 * Name: Laura Ruis
 * Student number: 10158006
 * Programmeerproject
 * VAST Challenge 2017
 */

window.onload = function() {

    var width = 1000,
        height = 1000;

    var svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height);

    var g = svg.append("g")
        .attr("class", "everything");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    // add zoom capabilities
    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    // set scale for nodes
    var nodeScale = d3.scaleLog();

    d3.json("../Data/graph.json", function(error, graph) {

        if (error) throw error;

        var link = g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line");

        var node = g.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("r", 5)
            .attr("fill", function(d) { return color(d.group); })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        console.log(d3.extent(graph.nodes, function(d) { return d.check_ins }));
        nodeScale
            .domain(d3.extent(graph.nodes, function(d) { return d.check_ins }));
        node.append("title")
            .text(function(d) { return d.id; });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function (d) {
                    return d.source.xpos * 4;
                })
                .attr("y1", function (d) {
                    return d.source.ypos * 4;
                })
                .attr("x2", function (d) {
                    return d.target.xpos * 4;
                })
                .attr("y2", function (d) {
                    return d.target.ypos * 4;
                });

            node
                .attr("r", function(d) { return nodeScale(d.check_ins)*20;})
                .attr("cx", function (d) {
                    return d.xpos * 4;
                })
                .attr("cy", function (d) {
                    return d.ypos * 4;
                })
                .on("mouseover", function(d) {
                    link.style("stroke", function(l) {
                        if (d === l.source || d === l.target)
                            return "#b40009";
                        else
                            return "grey";
                    });
                })
                .on('mouseout', function() {
                    link.style('stroke', "grey");
                });
        }
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.xpos * 4;
        d.fy = d.ypos * 4;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    //Zoom functions
    function zoom_actions(){
        g.attr("transform", d3.event.transform)
    }

};
