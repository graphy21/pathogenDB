from django.shortcuts import render
from django.http import HttpResponse
import os


def index(request):
	PATH_SOURCE = os.path.dirname(os.path.abspath(__file__))
	#return render(request, '{}/index.html'.format(PATH_SOURCE))
	return render(request, 'pathogenDB/index.html')
