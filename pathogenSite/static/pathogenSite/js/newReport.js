
$(document).ready(function () {

	function parseDataForDC(preData) {
		var data = [];
		for (var k in preData){
			if (preData.hasOwnProperty(k)){
				var datum = preData[k];
				for (var i = 0, max = datum.length; i < max; i += 1){
					data = data.concat(datum[i]);
				}
			}
		}
		return data;
	}

	function sampleTotalCount(data){
		var totalCount = {}
		for (var sample in data){
			totalCount[sample] = 0;
			var datum = data[sample];
			for (var i=0, max=datum.length; i < max; i += 1){
				totalCount[sample] += datum[i]['count'];
			}
		}
		return totalCount; // {sample1:count, sample2: count}
	}

	
	var totalCount = sampleTotalCount(oriData);
	var data = parseDataForDC(oriData);
	var sampleList = [];
	for (var sample in oriData) { sampleList.push(sample); }



	
	/*****
	 ***** model
	 *****/
	var model = { cr: crossfilter(data) };
	model.sampleDim = model.cr.dimension(function (d) {return d.sample;});
	model.sampleDimGroup = model.sampleDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.samplePerPathogenDimGroup = model.sampleDim.group().reduce(
		function (p, d) {
			if (d.pathogen_human == 3){ p.human_primary += d.count;
			} else if (d.pathogen_human == 4){p.human_opportunistic += d.count;}
			if (d.pathogen_animal == 3){ p.animal_primary += d.count;
			} else if (d.pathogen_animal == 4){p.animal_opportunistic+=d.count;}
			if (d.pathogen_plant == 3){ p.plant_primary += d.count;
			} else if (d.pathogen_plant == 4){p.plant_opportunistic += d.count;}
			return p;
		},
		function (p, d) {
			if (d.pathogen_human == 3){ p.human_primary -= d.count;
			} else if (d.pathogen_human == 4){p.human_opportunistic -= d.count;}
			if (d.pathogen_animal == 3){ p.animal_primary -= d.count;
			} else if (d.pathogen_animal == 4){p.animal_opportunistic-=d.count;}
			if (d.pathogen_plant == 3){ p.plant_primary -= d.count;
			} else if (d.pathogen_plant == 4){p.plant_opportunistic -= d.count;}
			return p;
		},
		function () {
			return {human_primary:0, human_opportunistic:0, animal_primary:0,
			animal_opportunistic:0, plant_primary:0, plant_opportunistic:0};
		}
	);
	model.pathogenDim = model.cr.dimension(function (d){return d.is_pathogen;});
	model.ranks = ["phylum", "class", "order", "family", "genus", "species"];
	model.allOrganismOptions = ["human_primary", "human_opportunistic", 
		"animal_primary", "animal_opportunistic", 
		"plant_primary", "plant_opportunistic"];
	model.colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3",
		"#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", 
		"#ffed6f"];
	model.legendColors = {human_primary:"red", human_opportunistic:"pink",
		animal_primary:"yellow", animal_opportunistic:"green",
		plant_primary:"blue", plant_opportunistic:"deepskyblue"
	};

	for (var i=0, max=model.ranks.length; i<max; i+=1){
		var rank = model.ranks[i];
		model[rank+"Dim"] = model.cr.dimension(function (d) {return d[rank];});
		model[rank+"DimGroup"] = model[rank+"Dim"].group().reduceSum(
			//function (d) {return d.count / totalCount[d.sample];}
			function (d) {return d.count;}
		);
		model[rank+"DimGroupInfo"] = model[rank+"Dim"].group().reduce(
			function (p, d) {
				p.count += d.count;
				p.pathogen_human = d.pathogen_human;
				p.pathogen_animal = d.pathogen_animal;
				p.pathogen_plant = d.pathogen_plant;
				return p;
			},
			function (p, d) {
				p.count -= d.count;
				p.pathogen_human = d.pathogen_human;
				p.pathogen_animal = d.pathogen_animal;
				p.pathogen_plant = d.pathogen_plant;
				return p;
			},
			function () {
				return {count:0, pathogen_human:"", pathogen_animal:"",
					pathogen_plant:""};
			}
		);
    }

	$.fn.dataTable.ext.type.order['count-with-percentage-pre'] = function (d) {
		return parseInt(d.split(" ")[0].replace(",",""));
	};

	var plot = { 
		mainPlot: dc.barChart("#main-plot"),
		mainTable: $("#main-table").DataTable({
			"columnDefs": [
				{
					//"render": function (data, type, row){
					//	return data.toString().replace(/\B(?=(\d{3})+(?!\d))/g,
					//	   	",") + " ( %)"
					//},
					"type": "count-with-percentage",
					"targets": 1
				}
			],
			"order": [[1, "desc"]]
		})
	};




	/*****
	 ***** controller
	 *****/
	var controller = {
		init: function () {
			view.init()
		},

		getColors: function () { return model.colors; },

		getLegendColors: function () { return model.legendColors; },

		getTableData: function(rank) {
			var selecteData = model[rank + "DimGroupInfo"].all();
			var tableData = [];
			var totalCount = 0;
			for (var i=0,max=selecteData.length; i<max; i+=1){
				var datum = selecteData[i],
					values = datum.value,
					count = values.count;
				totalCount += count;
			}
			for (var i=0,max=selecteData.length; i<max; i+=1){
				var datum = selecteData[i];
				var values = datum.value;
				var count = values.count;
				var countRender = values.count.toString()
					.replace(/\B(?=(\d{3})+(?!\d))/g, ",") + 
						" ( " + (count/totalCount*100).toFixed(2) + "%)";
				if (values.count != 0){
					if (rank === "species") {
						var pathogenInfo = {
							pathogen_human:"",
							pathogen_animal:"",
							pathogen_plant:""
						};
						var organisms = ["human", "animal", "plant"];
						for (var j=0,maxJ=organisms.length; j<maxJ; j+= 1){
							var organism = organisms[j];
							var index = "pathogen_"+organism;
							if (values[index] === "3") {
								pathogenInfo[index] = "primary";
							} else if (values[index] === "4") {
								pathogenInfo[index] = "opportunistic";
							} else {
								pathogenInfo[index] = "none";
							}
						}
					} else {
						var pathogenInfo = {
							pathogen_human:"-",
							pathogen_animal:"-",
							pathogen_plant:"-"
						}
					}
					tableData.push( [datum.key, countRender, 
							pathogenInfo["pathogen_human"], 
							pathogenInfo["pathogen_animal"],
							pathogenInfo["pathogen_plant"] ] );
				}
			}
			return tableData;
		},
		
		getAllOrganismOptions: function () { return model.allOrganismOptions; },

		getLineData: function() { 
			var resultData = {};
			var lineData = model.samplePerPathogenDimGroup.all();
			for (var i=0,max=lineData.length; i<max; i+=1){
				var lineDatum = lineData[i];
				resultData[lineDatum.key] = lineDatum.value;
			}
			return resultData;
		},
	
		filterByCheckedPathogenArray: function (checkedArray) {
			model.pathogenDim.filter(function (d) {
				return checkedArray.indexOf(d) > -1;
			});
		},

		getDataPerSample: function (rank, checkedArray, topNumber, yUnit) {
			// get top ranks 
			var topRanks = model[rank+"DimGroup"].top(topNumber);
			var topRankNames = [];
			var parsedData = [];
			for (var i=0, max=topRanks.length; i < max; i+=1){
				var topRank = topRanks[i];
				topRankNames.push(topRank['key']);
				parsedData.push( {key: topRank['key'], value: 
					this.getSampleDimGroupByType(rank, [topRank['key']], false,
						checkedArray, yUnit)
				});
			}
			parsedData.push({key:"etc", value:
				this.getSampleDimGroupByType(rank, topRankNames, true,
					checkedArray, yUnit)
			});
			return parsedData;

		},

		getSampleDimGroupByType: function(rank, types, exclude, checkPathogen,
				yUnit) {
			var group = model.sampleDim.group().reduceSum( function (d) {
				if ((exclude === true) && (types.indexOf(d[rank]) === -1)){
					if (yUnit === 'percentage') {
						return d.count / totalCount[d.sample];
					}
					return d.count;
				}else if ((exclude === false) && (types.indexOf(d[rank]) > -1)){
					if (yUnit === 'percentage') {
						return d.count / totalCount[d.sample];
					}
					return d.count;
				}
				return 0;
			});
			return group;
		}

	};




	/*****
	 ***** view
	 *****/
	var view = {
		init: function(){
			// set main plot
			var plotColors = controller.getColors();
			var mainPlot = plot.mainPlot;
			mainPlot
				.width(1100)
				.height(600)
				.margins({top:20, right:150, bottom:50, left:50})
				.x(d3.scale.ordinal().domain(sampleList))
				.xUnits(dc.units.ordinal)
				.brushOn(false)
				.xAxisLabel("Samples")
				.yAxisLabel("Percentage (%)")
				.elasticY(true)
				.dimension(model.sampleDim)
				.barPadding(0.1)
				.outerPadding(0.05)
				.transitionDuration(800)
				.renderHorizontalGridLines(true)
				.legend(dc.legend().x(950).y(20).itemHeight(13).gap(5)
					.horizontal(false).legendWidth(140).itemWidth(70))
				.group(model['sampleDimGroup']);
			mainPlot.ordinalColors( plotColors );
			mainPlot.yAxis().tickFormat(function(v) {
					return (v * 100).toFixed(2);});

			dc.renderAll();	
			var options = this.checkOptions();
			controller.filterByCheckedPathogenArray(options[1]);
			this.renderPlot(options[0], options[1], 5, options[2]);
			this.renderTable( controller.getTableData(options[0]) );

			// set each option event
			$("#unit-selector").change(function(){
				if ($(this).val() === "count"){
					mainPlot.elasticY(true)
						.yAxisLabel("Count");
					mainPlot.yAxis().tickFormat(function(v) {return v;});
				} else {
					mainPlot.elasticY(true)
						.yAxisLabel("Percentage (%)");
					mainPlot.yAxis().tickFormat(function(v) {
						return (v * 100).toFixed(2);});
				}
			});
			$("#plot-controller input[type=checkbox]").change(function(){
				var options = view.checkOptions();
				controller.filterByCheckedPathogenArray(options[1]);
			});
			// set options' common event
			$("#rank-selector, #unit-selector, input[type=checkbox]").on(
				"change", function () {
					var options = view.checkOptions();
					view.renderPlot(options[0], options[1], 5, options[2]);
					var tableData = controller.getTableData(options[0]);
					view.renderTable(tableData);
				}
			);
			// set event in main plot
			$("#main-plot").on("click", ".bar", function () {
				var options = view.checkOptions();
				var tableData = controller.getTableData(options[0]);
				view.renderTable(tableData);
			});

		},

		checkOptions: function (){
			var rank = $("#rank-selector").val();
			var yUnit = $("#unit-selector").val();
			var checkedArray = [];
			$("input:checked").each(function () {
				checkedArray.push($(this).val());
			});
			return [rank, checkedArray, yUnit];
		},

		checkOrganismOption: function () {
			var checkedArray = [];
			$(".organism:checked").each(function () {
				checkedArray.push($(this).val());
			});
			return checkedArray;
		},

		renderPlot: function (rank, checkedArray, topNumber, yUnit){
			var parsedData = controller.getDataPerSample(rank, checkedArray, 
					topNumber, yUnit);
			var mainPlot = plot.mainPlot;
			mainPlot
				.dimension(model.sampleDim)
				.on("renderlet", this.renderOverlaidLinePlot)
				.group(parsedData[0]['value'],parsedData[0]['key']);
			for (var i=1, max=parsedData.length; i < max; i += 1){
				var comp = parsedData[i];
				mainPlot.stack(comp['value'], comp['key']);
			}
			
			dc.redrawAll();
		},

		renderLineLegend: function () {
			var colors = controller.getLegendColors();
			var legendHeight = 5,
				legendWidth = 18,
				legendSpacing = 12,
				legendOffset = 430

			var allOrganismOptions = controller.getAllOrganismOptions();
			var organismOptions = view.checkOrganismOption();
			var colors = controller.getLegendColors();


			d3.select("svg").selectAll("g.legend").remove();

			var legend = d3.select("svg")
				.selectAll(".legend")
				.data(organismOptions)
				.enter().append("g")
				.attr("class", "legend")
				.attr("transform", function (d, i) {
					var y = legendOffset + 
						(legendHeight + legendSpacing) * i;
					return "translate(950," + y +")"; 
				});

			legend.append("rect")
				.attr("width", legendWidth)
				.attr("height", legendHeight)
				.style("fill", function (d) { return colors[d]; })
				.style("stroke", "none");

			legend.append("text")
				.attr("x", legendWidth + 4)
				.attr("y", 6)
				.text(function (d) { 
					d = d.replace("_", " ");
					d = d[0].toUpperCase() + d.slice(1) + " pathogen";
					return d; 
				});


		},

		renderOverlaidLinePlot: function (chart) {
			var options = view.checkOptions();
			var allOrganismOptions = controller.getAllOrganismOptions();
			var organismOptions = view.checkOrganismOption();
			var colors = controller.getLegendColors();
			var lineData = controller.getLineData();
			for (var i=0,max=allOrganismOptions.length; i<max; i+=1){
				var option = allOrganismOptions[i];
				var extraData = [];
				if (organismOptions.indexOf(option) > -1){
					for (var j=0,maxJ=sampleList.length; j<maxJ; j+=1){
						var sample = sampleList[j];
						var x = chart.x().range()[j] + chart.x().rangeBand()/2;
						if (options[2] === "count") {
							var y = chart.y()(lineData[sample][option]);
						} else {
							var y = chart.y()(lineData[sample][option]/
									totalCount[sample]);
						}
						extraData.push({x:x, y:y});
					}
				}
				// plot line
				var line = d3.svg.line() 
					.x(function(d) { return d.x; }) 
					.y(function(d) { return d.y; })
					.interpolate('linear');
				var path = chart.select('g.chart-body')
					.selectAll('path.'+option).data([extraData]);
				path.enter().append('path');
				path.attr('class', option)
					.attr('stroke', colors[option])
					.attr('d', line)
					.attr('stroke-width', 4)
					.attr('fill', 'none');
				//plot circle
				if ($("circle."+option).length) {
					chart.select('g.chart-body')
						.selectAll('circle.'+option)
						.data(extraData).exit().remove();
					chart.select('g.chart-body')
						.selectAll('circle.'+option)
						.attr("cx", function (d) { return d.x; })
						.attr("cy", function (d) { return d.y; });
				} else {
					var circle = chart.select('g.chart-body')
						.selectAll('circle.'+option)
						.data(extraData);
					circle.enter().append('circle')
						.attr('class', option).attr("r", 6)
						.attr("cx", function (d) { return d.x; })
						.attr("cy", function (d) { return d.y; })
						.attr("fill", colors[option])
						.attr("stroke","white")
						.attr("stroke-opacity","0.7")
						.attr("stroke-width", "3px");
				}
			}
			view.renderLineLegend();
		},

		renderTable: function (tableData) {
			var mainTable = plot.mainTable;
			mainTable
				.clear()
				.rows.add(tableData)
				.draw();
			$("tbody tr td:first-child").each(function () {
				$(this).html("<a target='_blank'"+
					"href='http://www.ezbiocloud.net/eztaxon/"+
					"hierarchy?m=nomen_view&nid="+$(this).text()+"'>"+
					$(this).text()+"</a>");

			});

		}
	};
	

	/*
	 * initialtion
	 */
	controller.init()

});
