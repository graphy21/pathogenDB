from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django import forms
from models import FastaFile, BlastResult, BlastLog


class IntroView(TemplateView):
	template_name = 'intro.html'
	pass


class UploadView(CreateView):
	pass


class MakeDbView(FormView):
	pass


class BlastView(FormView):
	pass
