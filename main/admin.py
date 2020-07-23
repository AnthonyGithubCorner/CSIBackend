from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from main.models import *

class CovidTestInline(admin.TabularInline):
    model = CovidTest
    extra = 0

class PatientAdmin(admin.ModelAdmin):
    inlines = [
        CovidTestInline,
    ]

admin.site.register(Patient, PatientAdmin)
admin.site.register(CovidTest)
admin.site.register(NewsArticle)
admin.site.register(ScientificArticle)
