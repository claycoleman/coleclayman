
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
    url(r'^choose_schedule/$', 'portfolio.views.choose_schedule', name='choose_schedule'),
    url(r'^ugf/$', 'portfolio.views.ugf', name='ugf'),
    url(r'^lds/page-checker/$', 'portfolio.views.check_page_number', name='check_page_number'),
    url(r'^lds/page-checker/json/$', 'portfolio.views.check_page_number_json', name='check_page_number_json'),
    url(r'^video/(?P<pk>\d+)/$', 'portfolio.views.video_call', name='video_call'),
    url(r'^video/(?P<pk>\d+)/(?P<slug>.+)/$', 'portfolio.views.video_call', name='video_call'),
    url(r'^video/ajax/$', 'portfolio.views.video_call_ajax', name='video_call_ajax'),
    url(r'^ajax/definition/$', 'portfolio.views.ajax_definition', name='ajax_definition'),
    url(r'^tz_detect/', include('tz_detect.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler500 = "portfolio.views.handler500"
