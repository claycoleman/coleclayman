
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', 'ugf.views.ugf_home', name='ugf_home'),
    url(r'^cra-checker/$', 'ugf.views.cra_checker', name='cra_checker'),  
    url(r'^meeting-buzzer/$', 'ugf.views.meeting_buzzer', name='meeting_buzzer'),  
    url(r'^meeting-buzzer/ping/$', 'ugf.views.meeting_buzzer_api_ping', name='meeting_buzzer_api_ping'),  
    url(r'^meeting-buzzer/ring/$', 'ugf.views.meeting_buzzer_api_ring', name='meeting_buzzer_api_ring'),  
    url(r'^deal-sourcing/$', 'ugf.views.deal_sourcing', name='deal_sourcing'),  
    url(r'^company-entry/$', 'ugf.views.company_entry', name='company_entry'),  
    url(r'^company-table/$', 'ugf.views.company_table', name='company_table'),  
    url(r'^login/$', 'ugf.views.login_view', name='login_view'),  
    url(r'^logout/$', 'ugf.views.logout_view', name='logout_view'),  
    url(r'^sign-up/$', 'ugf.views.signup_view', name='signup_view'),  

    # hubspot URLS
    url(r'^hubspot/$', 'ugf.views.hubspot', name='hubspot'),

    # airtable URLs
    url(r'^airtable_reports/$', 'ugf.views.airtable_reports', name='airtable_reports'),  
]
