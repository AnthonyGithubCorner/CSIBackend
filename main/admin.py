from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from main.models import *
from django.contrib.gis import admin as geo_admin


class CovidTestInline(admin.TabularInline):
    model = CovidTest
    extra = 0

class InsuranceInline(admin.TabularInline):
    model = Insurance
    extra = 0

class PatientAdmin(admin.ModelAdmin):
    inlines = [
        CovidTestInline,
        InsuranceInline,
    ]

admin.site.register(Point, geo_admin.GeoModelAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(CovidTest)
admin.site.register(NewsArticle)
admin.site.register(ScientificArticle)
admin.site.register(ModalityResource)

