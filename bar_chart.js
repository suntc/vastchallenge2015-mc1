data = [[12, 5, 8, 14, 28, 9, 31, 8, 1],
		[14, 4, 10, 32, 2, 15, 24, 7, 1],
		[9, 3, 7, 28, 6, 9, 42, 6, 1],
		[12, 4, 9, 9, 5, 8, 53, 6, 1],
		[38, 0, 12, 21, 1, 12, 21, 10, 1],
		[8, 3, 5, 9, 1, 10, 16, 4, 1],
		[11, 3, 7, 12, 6, 42, 22, 6, 1],
		[12, 3, 9, 11, 4, 25, 37, 7, 1],
		[37, 0, 14, 5, 2, 19, 30, 8, 1],
		[19, 3, 13, 13, 2, 10, 34, 10, 1]];

var bar_w = 600,
	bar_h = 1000,
	bar_start_Y = 100,
	single_chart_h = 200,
	single_bar_w = 20,
	height_ratio = 3;

var chartVis = d3.select("#bar_chart")
				.append("svg")
				.attr("width", bar_w)
				.attr("height", bar_h)

var charts = chartVis.selectAll(".bar")
					.data(data)
					.enter().append("g")
					.attr("class", "bar_chart")
					.attr("transform", function(d, i) {
						if (i >= 5)
							return "translate(260," + (single_chart_h * (i - 5) + bar_start_Y) + ")";
						else
							return "translate(0," + (single_chart_h * i + bar_start_Y) + ")";
					 })

var single_charts = charts.selectAll("g")
					 	.data(function(d) { return d; })
					 	.enter()

single_charts.append("rect")
	.attr("x", function(d, i) { return (single_bar_w + 2) * i; })
	.attr("y", function(d) { return -d * height_ratio; })
	.attr("width", single_bar_w)
	.attr("height", function(d) { return d * height_ratio; })
	.style("fill", function(d, i) {
		var colors = ["red", "steelblue", "pink", "lightseagreen", "midnightblue",
						"gold", "royalblue", "limegreen", "yellow"];
		return colors[i];
	})

single_charts.append("text")
	.attr("x", function(d, i) { return (single_bar_w + 2) * i; })
	.attr("y", 15)
	.style("font", "10px sans-serif")
	.text(function(d) { return d; })

single_charts.append("text")
	.attr("transform", "rotate(90)")
	.style("text-anchor", "end")
	.attr("x", -2)
	.attr("y", function(d, i) { return (single_bar_w + 2) * i - 180; })
	.text(function(d, i) {
		var types = ["Thrill", "Kiddle", "Everyone", "Shows",
		"Beer", "Food", "Shopping", "Restroom", "Infomation"];
		return types[8 - i];
	})
	.style("font", "10px sans-serif")