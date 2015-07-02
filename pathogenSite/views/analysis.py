import json

from django import forms
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from pathogenSite.models import Nomen, CLCSample

from CheckPathogen import Reporter


class PathogenAnalysis(TemplateView):
	template_name = 'pathogenSite/report/report.html'

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()
		clc_files = request.POST.getlist('sample')

		sample_index = 0
		total_micro_dist = []
		for clc_file in clc_files:
			sample_index += 1
			clc_file = json.loads(clc_file)
			file_path = clc_file['path']
			sample_name = clc_file['name']

			reporter = Reporter(file_path)
			reporter.check_rank_count()
			micro_dist = reporter.get_micro_dist()
			for comp in micro_dist:
				comp['sample'] = sample_name
				comp['i'] = sample_index
				total_micro_dist.append(comp)
			
	
		# Read Count Assignment Flow
		# Possible Pathogens & Diseases
		# Total Microbiome Distribution 
		# Pathogen Distribution
		# Pathogen Information
		context['well'] = reporter.get_clc_file()
		context['data'] = json.dumps(total_micro_dist)
		return super(PathogenAnalysis, self).render_to_response(context)

	def get_context_data(self, **kwargs): # this will be called 'GET' request
		context = super(PathogenAnalysis, self).get_context_data(**kwargs)
		return context


