// Load the Visualization API and the piechart package.
google.load('visualization', '1.1', 
	{'packages':['corechart', 'table', 'sankey']});

$("button.showReport").click(function (){
	if ($(this).text() === "Show Report"){
		$(this).parent().next().fadeToggle();
		$(this).text('Hide Report');
	} else {
		$(this).parent().next().fadeToggle();
		$(this).text('Show Report');
	}
});

$(document).ready(function () {
	$('.displayNone').hide(100);
});

var COLORS = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6",
	"#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11",
	"#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac",
	"#b77322", "#16d620", "#b91383", "#f4359e", "#9c5935", "#a9c413", "#2a778d",
	"#668d1c", "#bea413", "#0c5922", "#743411"];


for (var sample in oriData){
	var data = oriData[sample],
		divSankey = sample + "-div1-sankey1",
		totalData = parseData(data),
		dataSankey = totalData[0],
		divBubble = sample + "-div1-bubble1",
		dataBubble,
		divPie1 = sample + "-div2-pie1", 
		divPie2 = sample + "-div2-pie2",
		divTable1 = sample + "-div2-table1", 
		dataMChartGenus = totalData[1], 
		dataMChartSpecies = totalData[2],
		options = 
			{'title':'Genus', 'width':400, 'height':300, 'colors': COLORS}, 
		divPathogenPie = sample + "-div3-pie1",
		divPathogenColumn = sample + "-div3-column1",
		dataPathogenPie = totalData[3],
		dataPathogenColumn = totalData[4];
	


	dataBubble = { 
                "name": "Pathogen",
                "children": [
                    {"name": "endocarditis",
                    "children": [
                        {"name": "Streptococcus sanguinis", "size": 10},
                        {"name": "[GROUP] Escherichia coli", "size": 3},
                        {"name": "Granulicatella adiacens", "size": 2},
                        {"name": "Streptococcus mitis", "size": 11}
                        ]},
                    {"name": "Actinomycosis",
                    "children": [
                        {"name": "Actinomyces gerencseriae", "size": 2},
                        ]},
                    ]
                };

	/*
	dataPathogenPie = [
                [{"id":"","label":"level","pattern":"","type":"string"},
                {"id":"","label":"count","pattern":"","type":"number"}],
                ['NA',1000],
                ['Opportunistic Pathogen',17],
                ['Pathogen',9]
            ];

	dataPathogenColumn = [
                ['Pathogen', 'Pathogen', 'Opportunistic Pathogen',
                    { 'role': 'annotation' } ],
                ['Human', 3, 6, ''], ['Animal', 1, 0, ''], ['Plant', 0, 0, '']
            ]
	*/

	google.setOnLoadCallback( 
		drawTotalChartCallBack(divSankey, dataSankey)
	);
	drawBubbleChart(divBubble, dataBubble);
	google.setOnLoadCallback(
		drawMicrobiomeChartCallBack(divPie1, divPie2, divTable1, 
			dataMChartGenus, dataMChartSpecies, options)
	);
	google.setOnLoadCallback(
		drawPathogenChartCallBack(divPathogenPie, divPathogenColumn, 
			dataPathogenPie, dataPathogenColumn)
	);
	//showConnectivity();

}
function drawTotalChartCallBack(divSankey, dataSankey){
	return function () { drawTotalChart( divSankey, dataSankey ); };
}
function drawMicrobiomeChartCallBack (divPie1, divPie2, divTable1, 
	dataMChartGenus, dataMChartSpecies, options) {
	return function () { 
		drawMicrobiomeChart(divPie1, divPie2, divTable1, dataMChartGenus, 
			options, dataMChartSpecies);
	};
}
function drawPathogenChartCallBack(divPie, divColumn, dataPie, dataColumn) {
	return function () {
		drawPathogenChart(divPie, divColumn, dataPie, dataColumn);
	};
}

function parseData (data){
	// make sankeyData
	var sankeyData = [
		 [{"label":"From", "type":"string"}, 
			{"label":"to", "type":"string"}, 
			{"label":"read count", "type":"number"}]
		],
		genusData = [
			[{"id":"","label":"Genus","pattern":"","type":"string"},
			{"id":"","label":"count","pattern":"","type":"number"}],
		],
		speciesData = {
		},
		pathogenPieData = [
			[{"id":"","label":"level","pattern":"","type":"string"},
			{"id":"","label":"count","pattern":"","type":"number"}]
		],
		pathogenColumnData = [
			['Pathogen', 'Definitive Pathogen', 'Opportunistic Pathogen', 
				{ 'role': 'annotation' } ]
		],
		cf = crossfilter(data),
		genusDim = cf.dimension( function (d) { return d.genus; } ),
		genusDimGroup = genusDim.group().reduce(
			function (p, d) {
				p.count += d.count;
				p.species[d.species] = d.count;
				return p;
			},
			function (p, d) {
				p.count -= d.count;
				delete p.species[d.species];
				return p;
			},
			function () { return { 'count':0, 'species':{} } }
		),
		genus = genusDimGroup.all(),
		speciesDim = cf.dimension( function (d) { return d.species; } ),
		speciesDimGroup = speciesDim.group().reduce(
			function (p, d) { 
				if (d.pathogen_human != 0) {
					p.pathogen.push('Human Pathogen'); 
				}
				if (d.pathogen_animal != 0) {
					p.pathogen.push('Animal Pathogen'); 
				}
				if (d.pathogen_plant != 0) {
					p.pathogen.push('Plant Pathogen'); 
				}
				p.count += d.count; 
				return p;
			},
			function (p, d) { 
				if (d.pathogen_human != 0) {
					p.pathogen.splice(p.pathogen.indexOf('Human Pathogen'), 1); 
				}
				if (d.pathogen_animal != 0) {
					p.pathogen.splice(p.pathogen.indexOf('Animal Pathogen'), 1);
					p.pathogen.push('Animal Pathogen'); 
				}
				if (d.pathogen_plant != 0) {
					p.pathogen.splice(p.pathogen.indexOf('Plant Pathogen'), 1); 
				}
				p.count -= d.count; 
				return p;
			},
			function () { return {'count':0, 'pathogen':[]}; }
		),
		species = speciesDimGroup.all(),
		pathogenDim = cf.dimension( function (d) { return d.is_pathogen; } ),
		pathogenDimGroup = pathogenDim.group().reduceSum( function (d) {
			return d.count;
		}),
		pathogenAll = pathogenDimGroup.all(),
		pathogenOrganisms = {},
		humanPathogenDim = cf.dimension( function (d) {
			return d.pathogen_human;
		}),
		humanPathogenDimGroup = humanPathogenDim.group().reduceSum( function(d){
			return d.count;
		}),
		animalPathogenDim=cf.dimension(function(d){return d.pathogen_animal;}),
		animalPathogenDimGroup=animalPathogenDim.group().reduceSum(function(d){
			return d.count;
		}),
		plantPathogenDim = cf.dimension(function(d){return d.pathogen_plant;}),
		plantPathogenDimGroup = plantPathogenDim.group().reduceSum(function(d){
			return d.count;
		});
	
	pathogenOrganisms['Human'] = humanPathogenDimGroup.all();
	pathogenOrganisms['Animal'] = animalPathogenDimGroup.all();
	pathogenOrganisms['Plant'] = plantPathogenDimGroup.all();

	for (var i = 0, max = genus.length; i < max; i += 1){
		sankeyData.push(['total read', genus[i].key, genus[i].value.count ]);
		genusData.push([genus[i].key, genus[i].value.count]);
		speciesData[genus[i].key] = [
			[{"id":"","label":"Genus","pattern":"","type":"string"},
			{"id":"","label":"count","pattern":"","type":"number"}]
		];
		for (var k in genus[i].value.species){
			sankeyData.push( [genus[i].key, k, genus[i].value.species[k]] );
			speciesData[genus[i].key].push( [k, genus[i].value.species[k]] );
		}
	}
	for (var i = 0, max = species.length; i < max; i += 1){
		var pathogen = species[i].value.pathogen;
		if (pathogen.length === 0){
			sankeyData.push(
					[species[i].key,'Non Pathogen',species[i].value.count]);
		} else {
			sankeyData.push(
					[species[i].key, 'Pathogen', species[i].value.count]);
		}
		for (var j = 0, max2 = pathogen.length; j < max2; j += 1){
			var to = pathogen[j];
			sankeyData.push(['Pathogen', to, species[i].value.count]);
		}
	}
	console.log('4444', pathogenAll);
	for (var i = 0, max = pathogenAll.length; i < max; i += 1){
		console.log('22', pathogenAll);
		pathogenPieData.push( [pathogenAll[i].key, pathogenAll[i].value] );
	}
	
	var pathogenCount = {
		'Human': {'Opportunistic Pathogen':0, 'Definitive Pathogen':0},
		'Animal': {'Opportunistic Pathogen':0, 'Definitive Pathogen':0},
		'Plant': {'Opportunistic Pathogen':0, 'Definitive Pathogen':0}
	};
	for (var organism in pathogenOrganisms){
		var p = pathogenOrganisms[organism];
		for (var i = 0, max = p.length; i < max; i += 1){
			if (p[i].key == '3'){
				pathogenCount[organism]['Opportunistic Pathogen'] = p[i].value;
			} else if (p[i].key == '4'){
				pathogenCount[organism]['Definitive Pathogen'] = p[i].value;
			}
		}
		pathogenColumnData.push( [
				organism, 
				pathogenCount[organism]['Definitive Pathogen'], 
				pathogenCount[organism]['Opportunistic Pathogen'],
				''
		]);
	}
	console.log('1111', pathogenPieData);
	return [sankeyData, genusData, speciesData, pathogenPieData, 
		   pathogenColumnData];
}

function ColorLuminance (hex, lum) {
	// validate hex string
	hex = String(hex).replace(/[^0-9a-f]/gi, '');
	if (hex.length < 6) {
		hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
	}
	lum = lum || 0;

	// convert to decimal and change luminosity
	var rgb = "#", c, i;
	for (i = 0; i < 3; i++) {
		c = parseInt(hex.substr(i*2,2), 16);
		c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
		rgb += ("00"+c).substr(c.length);
	}
	return rgb;
}

function MakeGradientColors (hex, count){
	count = count;
	var diff = 1/count;
	var colors = [];
	for (i=0; i < count; i++){
		colors.push(ColorLuminance(hex, diff*i));
	};
	return colors;
}


//// 1.1 Read Count Assignment Flow
function drawTotalChart(div, data){
	var data = new google.visualization.arrayToDataTable( data ),
		colors = ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6', 
			'#ffff99', '#1f78b4', '#33a02c'],
		options = {width: 800, height: 1200, sankey:{'node': {'colors':colors},
			'link':{'colorMode':'gradient', 'colors':colors}
		}},
		sankey1 = new google.visualization.Sankey(
			document.getElementById(div)
		);
	sankey1.draw(data, options);	
};

//// 1.2 Possible Pathogens & Diseases
function drawBubbleChart(div, data){
	var margin = 30,
		diameter = 400;

	var color = d3.scale.linear()
		.domain([-1, 5])
		.range(["hsl(0,70%,85%)", "hsl(0,85%,55%)"])
		.interpolate(d3.interpolateHcl);

	var pack = d3.layout.pack()
		.padding(2)
		.size([diameter - margin, diameter - margin])
		.value(function(d) { return d.size; });

	var svg = d3.select(div).append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.append("g")
		.attr("transform", "translate(" +
			diameter / 2 + "," + diameter / 2 + ")");

	var root = data;

	var focus = root,
		nodes = pack.nodes(root),
		view;

	var circle = svg.selectAll("circle")
		.data(nodes)
		.enter().append("circle")
		.attr("class", function(d) { 
			return (d.parent ? d.children ? "node" : "node node--leaf" : 
				"node node--root"); 
		})
		.style("fill", function(d) { 
			return d.children ? color(d.depth) : null; 
		})
		.on("click", function(d) { 
			if (focus !== d)  zoom(d), event.stopPropagation();
		});

	var text = svg.selectAll("text")
		.data(nodes)
		.enter().append("text")
		.attr("class", "label")
		.classed("bubble", true)
		.style("fill-opacity", function(d) { 
			return d.parent === root ? 1 : 0; 
		})
		.style("display", function(d) { 
			return d.parent === root ? null : "none"; 
		})
		.text(function(d) { return d.name; });

	var node = svg.selectAll("circle,text");

	d3.select(div)
		.on("click", function() { zoom(root); });

	zoomTo([root.x, root.y, root.r * 2 + margin]);

	function zoom(d) {
		var focus0 = focus; focus = d;

		var transition = d3.transition()
			.duration(event.altkey ? 7500 : 750)
			.tween("zoom", function(d) { var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
				return function(t) { zoomTo(i(t)); };
			});

		transition.selectAll("text.bubble")
			.filter(function(d) {
				return d.parent === focus || this.style.display === "inline"; })
			.style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
			.each("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
			.each("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
	};

	function zoomTo(v) {
		var k = diameter / v[2]; view = v;
		node.attr("transform", function(d) {  return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
		circle.attr("r", function(d) { return d.r * k; });
	};
	d3.select(self.frameElement).style("height", diameter + "px");
};

//color = d3.scale.ordinal()
//.domain(["Human Pathogen", "Animal Pathogen", "Plant Pathogen"])
//.range(['#FE1E4D', '#5070FE', '#82FE8C']);


//// 2.1 Total Microbiome Distribution
function drawMicrobiomeChart(divPie1, divPie2, divTable1, data, options, 
	species_all) {
	// Create the data table.
	var data = new google.visualization.arrayToDataTable( data );
	var view = new google.visualization.DataView(data);

	// Set chart options
	//var options = {{ options|safe }};
	//var species_all = {{ species|safe }};

	// Instantiate and draw our chart, passing in some options.
	var chart1 = new google.visualization.PieChart(
		document.getElementById(divPie1));
	var chart2 = new google.visualization.PieChart(
		document.getElementById(divPie2));
	var table1 = new google.visualization.Table(
		document.getElementById(divTable1));

	google.visualization.events.addListener(table1, 'sort', 
		function(event) {
			order = data.getSortedRows(
				[{column: event.column, desc: !event.ascending}]);
			tablePreToCur = {};
			tableCurToPre = {};
			for (i=0; i < order.length; i++){
				tablePreToCur[order[i]] = i;
				tableCurToPre[i] = order[i];
			};
			data.sort([{column: event.column, desc: !event.ascending}]);
			chart1.draw(data, options);
	});

	google.visualization.events.addListener(table1, 'select', function() {
		selection = table1.getSelection();
		if (selection.length > 0){
			if (typeof(tablePreToCur) !== 'undefined'){
				rowNum = tablePreToCur[selection[0].row];
			}else{
				rowNum = selection[0].row;
			};
			chart1.setSelection([{'column':null, 'row':rowNum}]);
			genus = data.getValue(rowNum,0);
			var species = 
				new google.visualization.arrayToDataTable(species_all[genus]);
			var initColor = options['colors'][rowNum];
			var gradientColors = MakeGradientColors(initColor, 
				species_all[genus].length);
			var options_tt = 
				{'title': 'species('+ genus +')', 'width':400, 'height':300,
				'colors': gradientColors};
			chart2.draw(species, options_tt);
		};
	});
	
	google.visualization.events.addListener(chart1, 'select', function() {
		selection = chart1.getSelection();
		if (selection.length > 0){
			if (typeof(tableCurToPre) !== 'undefined'){
				rowNum = tableCurToPre[selection[0].row];
			}else{
				rowNum = selection[0].row;
			};
			table1.setSelection([{'row':rowNum, column:null}]);
			genus = data.getValue(selection[0].row,0);
			var species = 
				new google.visualization.arrayToDataTable(species_all[genus]);
			var initColor = options['colors'][selection[0].row];
			var gradientColors = MakeGradientColors(initColor, 
				species_all[genus].length);
			var options_tt = {'title': 'species('+ genus +')', 'width':400, 'height':300, 'colors': gradientColors};
			chart2.draw(species, options_tt);
		};
	});

	table1.draw(data);
	$('#div2_table1 table').addClass('table');
	chart1.draw(data, options);
	var genus = data.getValue(0,0);
	var species = new 
		google.visualization.arrayToDataTable(species_all[genus]);
	var initColor = options['colors'][0];
	var gradientColors = 
		MakeGradientColors(initColor, species_all[genus].length)
	var options_tt = {'title': 'species('+ genus +')', 'width':400, 
		'height':300,'colors': gradientColors};
	chart2.draw(species, options_tt);
};

//// 2.2 Pathogen Distribution
function drawPathogenChart(divPie, divColumn, dataPie, dataColumn){
	var dataPie1 = new google.visualization.arrayToDataTable( dataPie );
	var pie1 = new google.visualization.PieChart(
		document.getElementById( divPie ));
	pie1.draw(dataPie1, {'title':'Pathogen Proportion', 'width':400, 
		'height':300, 'colors': ['#109618', '#ff9900', '#dc3912'],
		'slices': {1:{'offset':0.15}, 2:{'offset':0.2}}
	});

	var dataColumn1 = new google.visualization.arrayToDataTable( dataColumn);
	var column1 = new google.visualization.ColumnChart(
		document.getElementById( divColumn ));
	column1.draw(dataColumn1, {'title':'Pathogens in Organisms', 'width':500, 
		'height':300, 'colors': ['#dc3912', '#ff9900'], 
		'legend':{'position':'right'}, 'isStacked':true, 
	});
};

//// 2.3 Pathogen Information
function showConnectivity(){
	$(".group").click(function(){
		$(".composition").fadeToggle();
	});

	///var data = {{ group|safe }}

	var width = 460,
		height = 250
		 
	var svg = d3.select(".composition").append("svg")
		.attr("width", width)
		.attr("height", height);
		 
	var force = d3.layout.force()
		.gravity(.05)
		.distance(100)
		.charge(-100)
		.size([width, height]);

	force
	  .nodes(data.nodes)
	  .links(data.links)
	  .start();
		 
	var link = svg.selectAll(".link")
	  .data(data.links)
	.enter().append("line")
	  .attr("class", "link");
		 
	var node = svg.selectAll(".node")
	  .data(data.nodes)
	  .enter().append("g")
	  .attr("class", "node")
	  .call(force.drag);
		 
	node.append("image")
	  .attr("xlink:href", "http://icons.iconarchive.com/icons/banzaitokyo/medico/48/bacteria-icon.png")
	  .attr("x", -8)
	  .attr("y", -8)
	  .attr("width", 16)
	  .attr("height", 16);
		 
	node.append("text")
	  .attr("dx", 12)
	  .attr("dy", ".35em")
	  .text(function(d) { return d.name });
		 
	force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
			 
		node.attr("transform", function(d) { 
			return "translate(" + d.x + "," + d.y + ")"; });
	});
};
$('.composition').hide()
