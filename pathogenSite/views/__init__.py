from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import (TemplateView, FormView, CreateView, ListView,
		DetailView, UpdateView)
from django.template.loader import render_to_string
from django import forms
from django.forms import ModelForm

import copy

from pathogenSite.models import Nomen, CLCSample


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
		self.fields['pathogen_human'].required = False


def make_prev_url(info, key):
	prev_url = []
	for k,v in info.items():
		if k != key:
			prev_url.append('{}={}'.format(k,v))
	return '&'.join(prev_url)


class PathogenList(ListView):
	model = Nomen
	template_name = 'pathogenSite/pathogen_list.html'
	context_object_name = 'pathogen_list'
	paginate_by = 15

	def get_queryset(self):
		params = copy.deepcopy(self.request.GET)
		if 'page' in params: params.pop('page')
		queryset = super(PathogenList, self).get_queryset()
		#self.form = PathogenListForm(self.request.GET or None)
		self.form = PathogenListForm(params or None)
		if self.form.is_valid():
			name = self.form.cleaned_data.get('name')
			if name:
				queryset = queryset.filter(name__contains=name)
			pathogen_human = self.form.cleaned_data.get('pathogen_human')
			if pathogen_human:
				queryset = queryset.filter(pathogen_human=pathogen_human)
		return queryset

	def get_context_data(self, **kargs):
		params = copy.deepcopy(self.request.GET)
		context = super(PathogenList, self).get_context_data(**kargs)
		context['form'] = self.form
		prev_url = make_prev_url(params, 'page')
		context['prev_url'] = prev_url
		context['clicked_nav'] = "pathogen_list"
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


class CLCSampleUploadForm(ModelForm):
	class Meta:
		model = CLCSample
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(CLCSampleUploadForm, self).__init__(*args, **kwargs)
		#self.fields['clc_file'].required = False
	
	def clean(self):
		cleaned_data = super(CLCSampleUploadForm, self).clean()
		print '11111\n\n', cleaned_data, cleaned_data['owner']

	def is_valid(self):
		a = super(CLCSampleUploadForm, self).is_valid()
		print 'gggggggggggg\n\n',a, self.cleaned_data
		return a


class CLCSampleUploadFormView(FormView):
	template_name = 'pathogenSite/sample_upload_form.html'
	form_class = CLCSampleUploadForm
	#success_url = '/'
	success_url = reverse_lazy('sample')

	def form_valid(self, form):
		print '55555555555\n\n', self.request.POST, self.request.FILES
		form.save()
		return super(CLCSampleUploadFormView, self).form_valid(form)

	def get_context_data(self, **kargs):
		context = super(CLCSampleUploadFormView, self).get_context_data(**kargs)
		context['clicked_nav'] = "sample_upload"
		print '22222\n\n', context, dir(context['form']), '\n\n', context['form'].errors
		return context


class SampleListView(ListView):
	model = CLCSample
	template_name = 'pathogenSite/sample_list.html'
	context_object_name = 'sample_list'
	paginate_by = 15
	def get_context_data(self, **kargs):
		params = copy.deepcopy(self.request.GET)
		context = super(SampleListView, self).get_context_data(**kargs)
		#context['form'] = self.form
		prev_url = make_prev_url(params, 'page')
		context['prev_url'] = prev_url
		context['clicked_nav'] = "sample_list"
		return context
