from django.contrib import admin
from portfolio.models import *
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'client_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
        
admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoCall)
admin.site.register(ScriptureCache)
admin.site.register(PageNumber)