from django import forms
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from pathogenSite.models import Nomen, CLCSample

from CheckPathogen import Reporter


class PathogenAnalysis(TemplateView):
	template_name = 'pathogenSite/report/report.html'

	def post(self, request, *args, **kwargs):
		clc_files = request.POST.getlist('sample')
		if len(clc_files) > 1:
			pass
		clc_file = clc_files[0]
		reporter = Reporter(clc_file)
		context = self.get_context_data()

		# Read Count Assignment Flow
		# Possible Pathogens & Diseases
		# Total Microbiome Distribution 
		# Pathogen Distribution
		# Pathogen Information
		
		context['well'] = clc_file
		return super(PathogenAnalysis, self).render_to_response(context)

	def get_context_data(self, **kwargs): # this will be called 'GET' request
		context = super(PathogenAnalysis, self).get_context_data(**kwargs)
		return context


