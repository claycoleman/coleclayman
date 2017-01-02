
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    url(r'^$', 'blog.views.blog_home', name='blog_home'),
    url(r'^all/$', 'blog.views.all_posts', name='all_posts'),
    url(r'^upload_images/$', 'blog.views.upload_images', name='upload_images'),
    url(r'^p/(?P<slug>.+)/$', 'blog.views.post_detail', name='post_detail'),
]
