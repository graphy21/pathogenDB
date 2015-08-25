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
		return totalCount;
	}

	
	var totalCount = sampleTotalCount(oriData);
	var data = parseDataForDC(oriData);

	
	/*
	 * model
	 */
	var model = {
		cr: crossfilter(data)
	};
	model.sampleDim = model.cr.dimension(function (d) {return d.sample;})
	model.phylumDim = model.cr.dimension(function (d) {return d.phylum;});
	model.classDim = model.cr.dimension(function (d) {return d.class;});
	model.orderDim = model.cr.dimension(function (d) {return d.order;});
	model.familyDim = model.cr.dimension(function (d) {return d.family;});
	model.genusDim = model.cr.dimension(function (d) {return d.genus;});
	model.speciesDim = model.cr.dimension(function (d) {return d.species;});
	model.sampleDimGroup = model.sampleDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.phylumDimGroup = model.phylumDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.classDimGroup = model.classDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.orderDimGroup = model.orderDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.familyDimGroup = model.familyDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.genusDimGroup = model.genusDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});
	model.speciesDimGroup = model.speciesDim.group().reduceSum(function (d) {
		return d.count / totalCount[d.sample];
	});

	var plot = { mainPlot: dc.barChart("#main-plot")};


	/*
	 * controller
	 */
	var controller = {
		init: function () {
			view.init()
		},

		getData: function (rank, checkedArray, topNumber, yUnit) {
			var parsedData = [];
			console.log(rank, checkedArray, topNumber, yUnit);
			// get top ranks 
			var topRanks = model[rank+"DimGroup"].top(topNumber);
			var topRankNames = [];
			for (var i=0, max=topRanks.length; i < max; i+=1){
				topRank = topRanks[i];
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

			console.log(topRankNames);
			return parsedData;

		},

		getSampleDimGroupByType: function(rank, types, exclude, checkPathogen,
				yUnit) {
			var group = model.sampleDim.group().reduceSum( function (d) {
				if ((exclude === true) && (types.indexOf(d[rank]) === -1)){
					if ((typeof checkPathogen !== 'undefined') && 
						(checkPathogen.indexOf(d.is_pathogen) > -1)){
						if (yUnit === 'percentage') {
							return d.count / totalCount[d.sample];
						}
						return d.count;
					}
				}else if ((exclude === false) && (types.indexOf(d[rank]) > -1)){
					if ((typeof checkPathogen !== 'undefined') && 
						(checkPathogen.indexOf(d.is_pathogen) > -1)){
						if (yUnit === 'percentage') {
							return d.count / totalCount[d.sample];
						}
						return d.count;
					}
				}
				return 0;
			});
			/*
			group.all = (function(){
				var all = group.top(Infinity);
				console.log('222', all);
				return function() { return all; };
			})();
			*/
			return group;
		}

	};

	
	/*
	 * view
	 */
	var view = {
		init: function(){
			// set main plot
			var mainPlot = plot.mainPlot;
			mainPlot
				.width(1100)
				.height(600)
				.margins({top:20, right:150, bottom:50, left:50})
				.x(d3.scale.ordinal())
				.xUnits(dc.units.ordinal)
				.brushOn(false)
				.xAxisLabel("Samples")
				.yAxisLabel("Percentage (%)")
				.elasticY(true)
				.dimension(model.sampleDim)
				.barPadding(0.1)
				.outerPadding(0.05)
				.transitionDuration(1000)
				.renderHorizontalGridLines(true)
				.legend(dc.legend().x(950).y(20).itemHeight(13).gap(5)
						.horizontal(false).legendWidth(140).itemWidth(70))
				.group(model['sampleDimGroup']);
			mainPlot.yAxis().tickFormat(function(v) {
					return (v * 100).toFixed(2);});

			dc.renderAll();	
			var options = this.checkOptions();
			this.render(options[0], options[1], 5, options[2]);
			// set option event
			$("#rank-selector").change(function(){
				var options = view.checkOptions();
				view.render(options[0], options[1], 5, options[2]);
			});
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
				var options = view.checkOptions();
				view.render(options[0], options[1], 5, options[2]);

			});
			$("#plot-controller input[type=checkbox]").change(function(){
				var options = view.checkOptions();
				view.render(options[0], options[1], 5, options[2]);
			});
			// set plot event
			$("#main-plot").on("click", ".bar", function () {
				var selectedSamples = [];
				//$(".selected").each(function () {selectedSample.});
				console.log("good", $(this).text());
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
			//this.render(rank, checkedArray, 5, yUnit)

		},

		render: function (rank, checkedArray, topNumber, yUnit){
			var parsedData = controller.getData(rank, checkedArray, topNumber, 
					yUnit);
			console.log(parsedData);
			var mainPlot = plot.mainPlot;
			mainPlot
				.dimension(model.sampleDim)
				.group(parsedData[0]['value'],parsedData[0]['key']);
			for (var i=1, max=parsedData.length; i < max; i += 1){
				var comp = parsedData[i];
				mainPlot.stack(comp['value'], comp['key']);
			}
			
			dc.redrawAll();
		}
	};
	

	/*
	 * initialtion
	 */
	controller.init()

});
