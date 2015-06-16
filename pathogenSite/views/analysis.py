from django import forms
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, FormView

from pathogenSite.models import Nomen, CLCSample



class PathogenAnalysis(TemplateView):
	template_name = 'pathogenSite/temp.html'

	def post(self, request, *args, **kwargs):
		clc_file = request.POST['sample']
		return super(PathogenAnalysis, self).render_to_response({'well':'kkk'})

	def get_context_data(self, **kwargs): # this will call 'GET' request
		context = super(PathogenAnalysis, self).get_context_data(**kwargs)
		return context

