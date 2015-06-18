from django.views.generic import TemplateView
import json

COLORS = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6",\
		"#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99",\
		"#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262",\
		"#5574a6", "#3b3eac", "#b77322", "#16d620", "#b91383", "#f4359e",\
		"#9c5935", "#a9c413", "#2a778d", "#668d1c", "#bea413", "#0c5922",\
		"#743411"]


class ReportTest(TemplateView):
	#template_name = 'pathogenSite/report/test.html'
	template_name = 'pathogenSite/report/tt.html'

	def get_context_data(self, **kwargs): # this will call 'GET' request
		context = super(ReportTest, self).get_context_data(**kwargs)
		# Total Summary
		total_summary = [
				[{"label":"From", "type":"string"},
					{"label":"to", "type":"string"},
					{"label":"read count", "type":"number"}],
				['total read', 'Blautia', 4],
				['total read', 'Streptococcus', 17],
				['total read', 'Escherichia', 43],
				['total read', 'Lactobacillus', 17],
				['total read', 'Catenibacterium', 24],
				['Blautia', 'b1', 3],
				['Blautia', 'b2', 1],
				['Streptococcus', 's1', 7],
				['Streptococcus', 's2', 10],
				['Escherichia', 'e1', 11],
				['Escherichia', 'e2', 11],
				['Escherichia', 'e3', 11],
				['Escherichia', 'e4', 10],
				['Lactobacillus', 'l1', 7],
				['Lactobacillus', 'l2', 10],
				['Catenibacterium', 'c1', 7],
				['Catenibacterium', 'c2', 7],
				['Catenibacterium', 'c3', 10],
				['b1', 'NA', 3],
				['b2', 'NA', 1],
				['s1', 'NA', 7],
				['s2', 'Oppotunistic pathogen', 1],
				['s2', 'NA', 9],
				['e1', 'Oppotunistic pathogen', 2],
				['e1', 'Pathogen', 1],
				['e1', 'NA', 8],
				['e2', 'NA', 11],
				['e3', 'NA', 11],
				['e4', 'NA', 10],
				['l1', 'NA', 7],
				['l2', 'NA', 10],
				['c1', 'NA', 7],
				['c2', 'NA', 7],
				['c3', 'Pathogen', 1],
				['c3', 'NA', 9],
				['Oppotunistic pathogen', 'Human', 3],
				['Pathogen', 'Human Pathogen', 2],
				]
		context['total_summary'] = total_summary

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
				['NA',1000],\
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
