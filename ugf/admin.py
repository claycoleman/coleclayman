from django.contrib import admin
import django.apps

from .models import *

# class TopicAdmin(admin.ModelAdmin):
#     list_display = ('name', 'available')
# admin.site.register(Topic, TopicAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_retrieved', 'date_data_retrieved', 'valid_candidate', 'current_series')
admin.site.register(Company, CompanyAdmin)


for model in django.apps.apps.get_models():
    if 'ugf' in str(model):
        if model not in admin.site._registry:
            admin.site.register(model)

