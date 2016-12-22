"""project URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

urlpatterns = [
    url(r'^nimda/', include(admin.site.urls)),
    url(r'^p/(?P<slug>.+)/$', 'portfolio.views.project_detail', name='project_detail'),
    url(r'^$', 'portfolio.views.new_home', name='new_home'),
    url(r'^me/$', 'portfolio.views.bio', name='bio'),
    url(r'^vc/$', 'portfolio.views.vc', name='vc'),
    url(r'^projects/$', 'portfolio.views.projects', name='projects'),
    url(r'^ugf/$', 'portfolio.views.ugf', name='ugf'),
    url(r'^video/(?P<pk>\d+)/$', 'portfolio.views.video_call', name='video_call'),
    url(r'^video/(?P<pk>\d+)/(?P<slug>.+)/$', 'portfolio.views.video_call', name='video_call'),
    url(r'^video/ajax/$', 'portfolio.views.video_call_ajax', name='video_call_ajax'),
    url(r'^ajax/definition/$', 'portfolio.views.ajax_definition', name='ajax_definition'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler500 = "portfolio.views.handler500"
