from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, ListView
from django import forms
from django.forms import ModelForm

from pathogenSite.models import Nomen


class TestForm(forms.Form):
	name = forms.CharField(label="good", max_length=10)


class TestFormView(FormView):
	template_name = 'pathogenSite/test.html'
	form_class = TestForm

	def form_valid(self,form):
		return HttpResponse('good')


class PathogenForm(ModelForm):
	class Meta:
		model = Nomen
		fields = ['uid', 'name', 'pathogen_human', 'pathogen_animal',\
				'pathogen_plant',]


class PathogenList(ListView):
	model = Nomen
	template_name = 'pathogenSite/pathogen_list.html'
	paginate_by = 10


class PathogenDetailForm():
	pass


class PathogenEditView(TemplateView):
	template_name = 'pathogenSite/intro.html'

	pass

