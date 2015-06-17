from django.views.generic import TemplateView
import json

COLORS = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6",\
		"#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99",\
		"#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262",\
		"#5574a6", "#3b3eac", "#b77322", "#16d620", "#b91383", "#f4359e",\
		"#9c5935", "#a9c413", "#2a778d", "#668d1c", "#bea413", "#0c5922",\
		"#743411"]


class ReportTest(TemplateView):
	template_name = 'pathogenSite/report/test.html'

	def get_context_data(self, **kwargs): # this will call 'GET' request
		context = super(ReportTest, self).get_context_data(**kwargs)

		# Total Microbiome Distribution
		options = {'title':'Genus', 'width':400, 'height':300, 'colors': COLORS}
		genus = [\
				[{"id":"","label":"Genus","pattern":"","type":"string"},\
				{"id":"","label":"count","pattern":"","type":"number"}],\
				['Blautia',4],\
				['Streptococcus',17],\
				['Escherichia',43],\
				['Lactobacillus',17],\
				['Catenibacterium',24]
			]
		species = {'Blautia':[\
					[{"id":"","label":"Genus","pattern":"","type":"string"},\
					{"id":"","label":"count","pattern":"","type":"number"}],\
					['m1',3],\
					['m2',1]],\
				'Streptococcus':[\
					[{"id":"","label":"Genus","pattern":"","type":"string"},\
					{"id":"","label":"count","pattern":"","type":"number"}],\
					['o1',7],\
					['o2',10]],
				'Escherichia':[\
					[{"id":"","label":"Genus","pattern":"","type":"string"},\
					{"id":"","label":"count","pattern":"","type":"number"}],\
					['o1',11],\
					['o2',11],\
					['o3',11],\
					['o4',10]],
				'Lactobacillus':[\
					[{"id":"","label":"Genus","pattern":"","type":"string"},\
					{"id":"","label":"count","pattern":"","type":"number"}],\
					['z1',7],\
					['z2',10]],
				'Catenibacterium':[\
					[{"id":"","label":"Genus","pattern":"","type":"string"},\
					{"id":"","label":"count","pattern":"","type":"number"}],\
					['p1',7],\
					['p2',7],\
					['p3',10]],
				}
		context['options']	= json.dumps(options)
		context['genus'] = json.dumps(genus)
		context['species'] = json.dumps(species)

		# Pathogen Distribution
		pathogen_portion = [\
				[{"id":"","label":"level","pattern":"","type":"string"},\
				{"id":"","label":"count","pattern":"","type":"number"}],\
				['NA',3800],\
				['Opportunistic Pathogen',17],\
				['Pathogen',9],\
			]
		pathogen_organism = [ 
				['Pathogen', 'Pathogen', 'Opportunistic Pathogen', 
					{ 'role': 'annotation' } ], 
				['Human', 3, 6, ''], ['Animal', 1, 0, ''], ['Plant', 0, 0, '']
			] 
		context['pathogen_portion'] = pathogen_portion
		context['pathogen_organism'] = pathogen_organism


		return context
