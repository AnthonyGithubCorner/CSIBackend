from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from main.models import *


admin.site.register(Patient)
admin.site.register(CovidTest)
admin.site.register(NewsArticle)
admin.site.register(ScientificArticle)
