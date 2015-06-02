from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (TemplateView, FormView, CreateView, ListView,
		DetailView, UpdateView)
from django.template.loader import render_to_string
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


class PathogenListForm(ModelForm):
	"""
	uid = forms.IntegerField(label="uid")
	name = forms.CharField(label="Pathogen Name", max_length=500)
	pathogen_human = forms.IntegerField(label="Pathogen Human")
	"""
	class Meta:
		model = Nomen
		fields = ['name', 'pathogen_human']
	def __init__(self, *args, **kwargs):
		super(PathogenListForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = False


class PathogenList(ListView):
	model = Nomen
	template_name = 'pathogenSite/pathogen_list.html'
	context_object_name = 'pathogen_list'
	paginate_by = 10

	def get_queryset(self):
		queryset = super(PathogenList, self).get_queryset()
		self.form = PathogenListForm(self.request.GET or None)
		if self.form.is_valid():
			name = self.form.cleaned_data.get('name')
			if name:
				queryset = queryset.filter(name__contains=name)
			pathogen_human = self.form.cleaned_data.get('pathogen_human')
			if pathogen_human:
				queryset = queryset.filter(pathogen_human=pathogen_human)
		return queryset

	def get_context_data(self, **kargs):
		context = super(PathogenList, self).get_context_data(**kargs)
		context['form'] = self.form
		return context


class PathogenForm(ModelForm):
	class Meta:
		model = Nomen
		exclude = []	

class PathogenUpdateView(UpdateView):
	model = Nomen
	form_class = PathogenForm
	template_name = 'pathogenSite/pathogen_edit_form.html'
	slug_field = 'uid'

	def dispatch(self, *args, **kwargs):
		self.pathogen_uid = kwargs['slug']
		return super(PathogenUpdateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.save()
		pathogen = Nomen.objects.get(uid=self.pathogen_uid)
		return HttpResponse(render_to_string(\
				'pathogenSite/pathogen_success.html'), {'pathogen', pathogen})


class PathogenDetail(DetailView):
	model = Nomen
	slug_field = 'uid'
	template_name = "pathogenSite/pathogen_detail.html"


class PathogenEditView(TemplateView):
	template_name = 'pathogenSite/intro.html'
	pass

