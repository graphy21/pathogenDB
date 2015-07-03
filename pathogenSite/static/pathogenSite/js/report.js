/* handle event 
 * */
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

var data = parseDataForDC(oriData); // decide location of this variable !!

$('.exp').css('cursor', 'help');
$('.exp').tooltip({show: {effect:'Fade', duration:10}});
$('.row').css('margin-top','20px');
$(document).ready(function(){
	for (var k in indexToSample){
		if (indexToSample.hasOwnProperty(k)){
			var v = indexToSample[k];
			$('#sortable').append('<div class="btn ui-state-default">'+ 
				v +'</div>');
		}
	}
	$('#sortable').sortable();
	$('#sortable').disableSelection();
	$('#apply-sorting').click(function (){
		var order = [];
		$('#sortable').children().each(function () {
			order.push($(this).text());
		});

		// update "indexToSample", "sampleToIndex"
		for (var i = 0, max = order.length; i < max; i += 1) {
			indexToSample[i] = order[i];
			sampleToIndex[order[i]]	= i;
		}
		// update Chart
		speciesPerSampleBarChart.x(d3.scale.ordinal().domain(order));
		lineChart.x(d3.scale.ordinal().domain(order));
		dc.redrawAll();
	});
});

/* variables 
 * */
var topGenusCount = 5,
	topSpeciesCount = 7,

	samplePieChart = dc.pieChart('#sample-pie-chart'),
	genusPieChart = dc.pieChart('#genus-pie-chart'),
	speciesPieChart = dc.pieChart('#species-pie-chart'),
	speciesPerSampleBarChart = dc.barChart('#sample-stack-chart'),
	lineChart = dc.lineChart('#sample-line-chart'),

	microbiome = crossfilter(data),
	all = microbiome.groupAll(),

	sampleDim = microbiome.dimension(function (d) {
		return d.sample;
	}),
	sampleDimGroup = sampleDim.group().reduceSum( function (d){
		return d.count;
	}),
	indexToSample = {},
	sampleToIndex = {},

	genusDim = microbiome.dimension(function (d){
		return d.genus;    
	}),                    
	genusDimGroup = genusDim.group().reduceSum(function (d) {
		return d.count;
	}),
	speciesDim = microbiome.dimension(function (d){
		return d.species;
	}),
	speciesDimGroup = speciesDim.group().reduceSum(function (d) {
		return d.count;
	}),

	topSpecies = speciesDimGroup.top(topSpeciesCount),
	topSpeciesName = [],

	speciesPerSamples = [],
	speciesPerSamples2 = [];

/* populate variables 
 * */
for (var i = 0, max = topSpecies.length; i < max; i +=1 ){
	topSpeciesName.push(topSpecies[i].key);
}

function getSampleDimGroupByType(rank, types, exclude) {
	var group = sampleDim.group().reduceSum( function (d) {
			if ((exclude === true) && (types.indexOf(d[rank]) === -1)){
				return d.count;
			} else if ((exclude === false) && (types.indexOf(d[rank]) > -1)){
				return d.count;
			} else {
				return 0;
			}
	});
	group.all = function(){
		var result = [];
		var tt = {};
		var ref = group.top(Infinity);
		for (var i = 0, max = ref.length; i < max; i+= 1){
			var sampleName = ref[i].key;
			var index = sampleToIndex[sampleName];
			tt[index] = ref[i];
		}
		for (var i = 0, max = ref.length; i < max; i += 1){
			result.push(tt[i]);
		}
		return result;
	}
	return group;
}

for (var i = 0, max = topSpeciesName.length; i < max; i += 1){
	var species = topSpeciesName[i];
	var value = getSampleDimGroupByType('species', [species], false);
	speciesPerSamples.push( {'key':species, 'value': value} );
}

speciesPerSamples.push({'key': 'etc', 'value': 
		getSampleDimGroupByType('species', topSpeciesName, true)});

for (var i=0, max=sampleDimGroup.all().length; i < max; i += 1){
	var t = sampleDimGroup.all()[i];
	indexToSample[i] = t.key;
	sampleToIndex[t.key] = i;
}

/* draw chart 
 * */
samplePieChart
	.width(200)
	.height(200)
	.radius(90)
	.innerRadius(20)
	.dimension(sampleDim)
	.group(sampleDimGroup)
	.label(function (d) {
		return d.data.key;
	})
	.valueAccessor(function(d){
		return d.value;
	});

genusPieChart
	.width(200)        
	.height(200)       
	.radius(90)        
	.dimension(genusDim)
	.group(genusDimGroup);

speciesPieChart
	.width(200)        
	.height(200)       
	.radius(90)        
	.dimension(speciesDim)
	.group(speciesDimGroup);

speciesPerSampleBarChart
	.width(790)
	.height(300)
	.margins({top:20, right:20, bottom:30, left:50})
	.dimension(sampleDim)
	.group(speciesPerSamples[0]['value'], speciesPerSamples[0]['key'])
	.valueAccessor(function(p) {
		return p.value;
	});

for (var i = 1, max = speciesPerSamples.length; i < max; i+=1){
	var comp = speciesPerSamples[i];
	speciesPerSampleBarChart.stack(comp['value'], comp['key']);
}
speciesPerSampleBarChart
	.x(d3.scale.ordinal())
	.xUnits(dc.units.ordinal)
	.elasticX(true)
	.elasticY(true)
	.centerBar(true)
	.gap(5)
	.renderHorizontalGridLines(true)
	.title(function(d){
		return d.y;
	});

lineChart
	.renderArea(true)
	.xUnits(dc.units.ordinal)
	.width(790)
	.height(300)
	.margins({top:20, right:20, bottom:30, left:50})
	.dimension(sampleDim)
	.valueAccessor(function(p){
		return p.value;
	})
	.group(speciesPerSamples[0]['value'], speciesPerSamples[0]['key']);
for (var i = 1, max = speciesPerSamples.length; i < max; i+=1){
	var comp = speciesPerSamples[i];
	lineChart.stack(comp['value'], comp['key']);
}

lineChart
	.renderHorizontalGridLines(true)
	.x(d3.scale.ordinal())
	.xUnits(dc.units.ordinal)
	.elasticX(true)
	.elasticY(true);


dc.renderAll();
