from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (TemplateView, FormView, CreateView, ListView,
		DetailView, UpdateView)
from django.template.loader import render_to_string
from django import forms
from django.forms import ModelForm

import copy

from ssuProkSite.models import TaxGroup


class IntroView(TemplateView):
	template_name = 'ssuProkSite/intro.html'


class TaxonGroupQueryForm(ModelForm):
	class Meta:
		model = TaxGroup
		fields = ['group_name', 'tax_list']

	def __init__(self, *args, **kwargs):
		super(TaxonGroupQueryForm, self).__init__(*args, **kwargs)
		self.fields['group_name'].required = False
		self.fields['tax_list'].required = False



class TaxonGroupListView(ListView):
	model = TaxGroup
	template_name = 'ssuProkSite/tax_group_list.html'
	context_object_name = 'tax_group_list'
	paginate_by = 15

	def get_queryset(self):
		params = copy.deepcopy(self.request.GET)
		if 'page' in params: params.pop('page')
		queryset = super(TaxonGroupListView, self).get_queryset()
		self.form = TaxonGroupQueryForm(params or None)
		if self.form.is_valid():
			group_name = self.form.cleaned_data.get('group_name')
			if group_name:
				queryset = queryset.filter(group_name__icontains=group_name)
			tax_list = self.form.cleaned_data.get('tax_list')
			if tax_list:
				queryset = queryset.filter(tax_list__icontains=tax_list)
		return queryset

	def get_context_data(self, **kargs):
		context = super(TaxonGroupListView, self).get_context_data(**kargs)
		context['form'] = self.form
		context['form_head'] = ['Group Name', 'Tax List', 'Additional Information', 'Comment']
		return context


class TaxonGroupForm(ModelForm):
	class Meta:
		model = TaxGroup
		exclude = []	


class TaxonGroupUpdateView(UpdateView):
	model = TaxGroup
	form_class = TaxonGroupForm
	template_name = 'ssuProkSite/tax_group_edit_form.html'
	slug_field = 'uid'

	def dispatch(self, *args, **kwargs):
		self.taxon_group_uid = kwargs['slug']
		return super(TaxonGroupUpdateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.save()
		taxon_group = TaxGroup.objects.get(uid=self.taxon_group_uid)
		print '22222\n\n', taxon_group
		return HttpResponse(render_to_string(\
				'ssuProkSite/tax_group_success.html'),\
				{'taxon_group', taxon_group})


