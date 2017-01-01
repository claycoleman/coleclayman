
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    url(r'^$', 'blog.views.blog_home', name='blog_home'),
    url(r'^p/(?P<slug>.+)/$', 'blog.views.post_detail', name='post_detail'),
]
