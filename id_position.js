var id_position_w = 680,
	dh = 15,
	dw = 6,
 	beginY = 60,
	beginX = 80,
	sitesPerHour = 6,
	tw = dw * sitesPerHour * 16;

refreshGraph({});

function showGroupDetail(p)
{
	selectActionData(lbDbGroup[idDbGroup[p['id']].toString()])
}

function refreshGraph(actionData) {
	// Given new data, refresh the graph
	d3.select('#id_position').select('svg').remove();

	var vis = d3.select("#id_position")
		.append("svg")
    	.attr("width", id_position_w)
		.attr("height", beginY + Object.keys(actionData).length * (dh + 4));

	var bars = vis.selectAll(".bar")
		.data(actionDataArray(actionData))
	    .enter().append("g")
		.attr("class", "bar")
		.attr("person_id", function(d) { return d.id; })
		.attr("transform", function(d, i) { return "translate(0," + (i * (dh + 4) + beginY) + ")"; })
		.on("click",showGroupDetail);
		
	bars.append("rect")
		.attr("x", beginX)
		.attr("height", dh)
		.attr("width", tw)
		.style("fill", "whitesmoke");
		
	bars.each(Bar);

	bars.append("text")
		.attr("class", "bar_text")
		.attr("alignment-baseline", "baseline")
		.text(function(d) { return d.id; });

	// Add time label
	var column = vis.selectAll(".time")
		.data(d3.range(8, 25))
		.enter().append("g")
		.attr("class", "time")
		.attr("transform", function(d, i) { return "translate(" + (i * dw * sitesPerHour + beginX) + ",20)"; })
		.append("text").attr("class", "bar_text")
		.text(function(d) { return d; })
}

function getColor(d, i) {
	return "red";
}

function actionDataArray(actionData) {
	array = []
	for (var dataId in actionData) {
		array.push({id: dataId, path: actionData[dataId]})
	}
	return array;
}

function Bar(bar) {
	var grid = d3.select(this).selectAll(".grid")
				.data(function(d) { return d.path.filter(getOdd); })
				.enter()
				.append("rect")
				.attr("class", "grid")
				.attr("x", function(d, i) { return i * dw + beginX; })
				.style("fill", getColor)
				.on("mouseover", function(d, i) {
					var person_id = d3.select(this.parentNode).attr("person_id")
					var points = trackData[person_id][i * 2];
					for (var i = 0; i < points.length; i++) {
						var point = points[i];
						addPoint(point[0], point[1], i / points.length);
					}
				})
				.on("mouseout", function(d, i) {
					var person_id = d3.select(this.parentNode).attr("person_id")
					var points = trackData[person_id][i * 2];
					for (var point of points)
						removePoint(point[0], point[1]);
				});
}

function getOdd(d, i) {
	return i % 2 == 0
}

var getColor = (function() {
	lastColor = "whitesmoke";
	return function(d) {
		switch (d) {
		case -1:
			lastColor = "whitesmoke";
			return "whitesmoke";
		case 0:
			return lastColor;   // moving
		case 1: case 2: case 3: case 4: case 5: case 6: case 7: case 8: case 81:
			// thrill rides
			lastColor = "red";
			return "red";
		case 9: case 10: case 11: case 12: case 13: case 14: case 15: case 16:
		case 17: case 18: case 19:
			// kiddle rides
			lastColor = "steelblue";
			return "steelblue";
		case 20: case 21: case 22: case 23: case 24: case 25: case 26: case 27:
		case 28: case 29: case 30: case 31:
			// rides for everyone
			lastColor = "pink";
			return "pink";
		case 35: case 36: case 37: case 38: case 39: case 53: case 54: case 55:
		case 56: case 57: case 58: case 59:
			// food
			lastColor = "lightseagreen";
			return "lightseagreen";
		case 49: case 50: case 51: case 52: case 65: case 66: case 67:
			// restrooms
			lastColor = "midnightblue";
			return "midnightblue";
		case 33: case 34:
			// beer
			lastColor = "gold";
			return "gold";
		case 40: case 41: case 42: case 43: case 44: case 45: case 46: case 47:
		case 48:
			// shopping
			lastColor = "royalblue";
			return "royalblue";
		case 32: case 63: case 64: case 61:
			// shows & entertainment
			lastColor = "limegreen";
			return "limegreen";
		case 60: case 62:
			// info & assistence
			lastColor = "yellow";
			return "yellow";
		default:
			lastColor = "black";
			return "black";
		}
	}
})()
