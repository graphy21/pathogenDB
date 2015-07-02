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
			console.log('vvvvvv',v);
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
		speciesPerSampleBarChart.x(d3.scale.ordinal().domain(order));
		lineChart.x(d3.scale.ordinal().domain(order)).renderArea(true);
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

	top_species = speciesDimGroup.top(topSpeciesCount),
	top_species_name = [],

	species_per_samples = [];

/* populate variables 
 * */
for (var i = 0, max = top_species.length; i < max; i +=1 ){
	top_species_name.push(top_species[i].key);
}

function getSampleDimGroupByType(rank, type) {
	return sampleDim.group().reduceSum( function (d) {
			if (d[rank] === type){
				return d.count;
			} else {
				return 0;
			}
		});}

for (var i = 0, max = top_species_name.length; i < max; i += 1){
	var species = top_species_name[i];
	var value = getSampleDimGroupByType('species', species);
	species_per_samples.push( {'key':species, 'value': value} );
}

species_per_samples.push({'key': 'etc', 'value': 
	sampleDim.group().reduceSum( function (d) {
			if (top_species_name.indexOf(d['species']) === -1){
				return d.count;
			} else {
				return 0;
			}
		})});

for (var i=0, max=sampleDimGroup.all().length; i < max; i += 1){
	var t = sampleDimGroup.all()[i];
	indexToSample[i] = t.key;
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
	.group(species_per_samples[0]['value'], species_per_samples[0]['key'])
	.valueAccessor(function(p) {
		return p.value;
	});

for (var i = 1, max = species_per_samples.length; i < max; i+=1){
	var comp = species_per_samples[i];
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
	.width(790)
	.height(300)
	.margins({top:20, right:20, bottom:30, left:50})
	.dimension(sampleDim)
	.valueAccessor(function(p){
		return p.value;
	})
	.group(species_per_samples[0]['value'], species_per_samples[0]['key']);

for (var i = 1, max = species_per_samples.length; i < max; i+=1){
	var comp = species_per_samples[i];
	lineChart.stack(comp['value'], comp['key']);
}
lineChart
	.renderHorizontalGridLines(true)
	.x(d3.scale.ordinal())
	.xUnits(dc.units.ordinal)
	.elasticX(true)
	.elasticY(true);


dc.renderAll();

