//function makeReport (data) {
//$(document).ready(function(){
	var pieChart = dc.pieChart('#sample-pie-chart');
	console.log('aaaaa', pieChart);
	var pieChartTest = dc.pieChart('#sample-pie-chart-test');
	var typeChart = dc.barChart('#sample-stack-chart');

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
	var genusDimGroup = genusDim.group();

	console.log('111111', sampleDimGroup.all());
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
		//.brushOn(false)
		.margins({top:20, right:20, bottom:30, left:50})
		.dimension(sampleDim)
		.group(sampleDimGroup)
		.x(d3.scale.ordinal())
		.xUnits(dc.units.ordinal)
		.elasticY(true)
		.centerBar(true)
		.gap(5)
		.renderHorizontalGridLines(true)
		.valueAccessor(function(d) {
			return d.value.count;
		});


	dc.renderAll();

//}

//});
