//function makeReport (data) {
//$(document).ready(function(){
	var topSpeciesCount = 5;
	var topGenusCount = 5;
	var pieChart = dc.pieChart('#sample-pie-chart');
	var pieChartTest = dc.pieChart('#sample-pie-chart-test');
	var typeChart = dc.barChart('#sample-stack-chart');
	var lineChart = dc.lineChart('#sample-line-chart');

	var microbiome = crossfilter(data);
	var all = microbiome.groupAll();

	var sampleDim = microbiome.dimension(function (d) {
		return d.sample;
	});
	var sampleDimGroup2 = sampleDim.group().reduceSum(function(d){
		return d.count;
	});
	var sampleDimGroup = sampleDim.group().reduce(
		function(p, v){
			p.count += v.count;
			return p;
		},
		function(p, v){
			p.count -= v.count;
			return p;
		},
		function(){return {count: 0};}
	);
	var genusDim = microbiome.dimension(function (d){
		return d.genus;    
	});                    
	var genusDimGroup = genusDim.group().reduceSum(function (d) {
		return d.count;
	});

	var top_genus = genusDimGroup.top(topGenusCount);
	var genus_per_samples = [];
	function getSampleDimGroupByGenus(genus) {
		return sampleDim.group().reduceSum(function(d){
			if (d.genus === genus){
				return d.count;
			} else {
				return 0;
			}
		});
	}
	for (var i=0;i < top_genus.length; i++){
		var genus = top_genus[i].key;
		var value = getSampleDimGroupByGenus(genus);
		genus_per_samples.push( {'key':genus, 'value': value} );
	}

	pieChart
		.width(200)
		.height(200)
		.radius(90)
		.innerRadius(20)
		.dimension(sampleDim)
		.group(sampleDimGroup2);

	pieChartTest           
		.width(200)        
		.height(200)       
		.radius(90)        
		.innerRadius(20)   
		.dimension(genusDim)
		.group(genusDimGroup);

	typeChart
		.width(790)
		.height(300)
		.margins({top:20, right:20, bottom:30, left:50})
		.dimension(sampleDim)
		.group(sampleDimGroup);

	for (var i=0; i< genus_per_samples.length; i++){
		var comp = genus_per_samples[i];
		typeChart.stack(comp['value'], comp['key']);
	}

	typeChart
		.x(d3.scale.ordinal())
		.xUnits(dc.units.ordinal)
		.elasticY(true)
		.centerBar(true)
		.gap(5)
		.renderHorizontalGridLines(true)
		.valueAccessor(function(d) {
			return d.value.count;
		})
		.title(function(d){
			return d.y;
		});

	lineChart
		.renderArea(true)
		.width(790)
		.height(300)
		.margins({top:20, right:20, bottom:30, left:50})
		.dimension(sampleDim)
		.group(sampleDimGroup, 'All');

	for (var i=0; i< genus_per_samples.length; i++){
		var comp = genus_per_samples[i];
		lineChart.stack(comp['value'], comp['key']);
	}
	lineChart
		.renderHorizontalGridLines(true)
		.x(d3.scale.ordinal())
		.xUnits(dc.units.ordinal)
		.elasticY(true)
		.valueAccessor(function(d){
			return d.value.count;
		});

	dc.renderAll();

//}

//});
