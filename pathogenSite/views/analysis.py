import json

from django import forms
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from pathogenSite.models import Nomen, CLCSample

from CheckPathogen import Reporter


class PathogenAnalysis(TemplateView):
	template_name = 'pathogenSite/report/new_report.html'
	#template_name = 'pathogenSite/report/report.html'

	def post(self, request, *args, **kwargs):
		"""
		total_micro_dist = {
		'sample1': [{'sample':, 'genus':, 'species':, 'count':, 'is_pathogen':,
			'pathogen_human':, 'pathogen_animal':, 'pathogen_plant':}],
		}
		"""
		context = self.get_context_data()
		clc_files = request.POST.getlist('sample')

		total_micro_dist = {}
		samples = []
		for clc_file in clc_files:
			clc_file = json.loads(clc_file)
			file_path = clc_file['path']
			sample_name = clc_file['name']
			samples.append(sample_name)

			reporter = Reporter(file_path)
			reporter.check_rank_count()
			micro_dist = reporter.get_micro_dist(end_rank='phylum')
			total_micro_dist[sample_name] = []
			for comp in micro_dist:
				comp['sample'] = sample_name
				total_micro_dist[sample_name].append(comp)
			
	
		# Read Count Assignment Flow
		# Possible Pathogens & Diseases
		# Total Microbiome Distribution 
		# Pathogen Distribution
		# Pathogen Information
		context['samples'] = samples
		context['data'] = json.dumps(total_micro_dist)
		return super(PathogenAnalysis, self).render_to_response(context)

	def get_context_data(self, **kwargs): # this will be called 'GET' request
		context = super(PathogenAnalysis, self).get_context_data(**kwargs)
		return context


