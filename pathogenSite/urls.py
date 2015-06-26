"""chunlab_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from pathogenSite import views
from pathogenSite.views.analysis import PathogenAnalysis
from pathogenSite.views.report import ReportTest


urlpatterns = [
	url(r'^$', login_required(views.PathogenEditView.as_view()),
		name='ezbio-intro'),
	url(r'^pathogen$', login_required(views.PathogenList.as_view()), 
		name='pathogen'),
	url(r'^pathogen/(?P<slug>\d+)$', 
		login_required(views.PathogenUpdateView.as_view()),
		name='pathogen_update'),
	url(r'^sample$', login_required(views.SampleListView.as_view()),
		name='sample'),
	url(r'^sample-upload$',
		login_required(views.CLCSampleUploadFormView.as_view()), 
		name='sample-upload'),
	url(r'^sample-analysis$',
		login_required(PathogenAnalysis.as_view()), 
		name='sample-analysis'),
	url(r'^report$',
		#login_required(ReportTest.as_view()), 
		ReportTest.as_view(), 
		name='report'),
	url(r'^test$', views.TestView.as_view(), name='test'),
]
