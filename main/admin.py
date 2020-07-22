from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from main.models import *



class PatientAdmin(admin.ModelAdmin):
    # pass what attributes to display and what search field will look for in admin
    list_display = ('status', 'user', '__str__')
    search_fields = ('status', 'user', '__str__')
    pass


admin.site.register(Patient, PatientAdmin)
admin.site.register(NewsArticle)
admin.site.register(ScientificArticles)