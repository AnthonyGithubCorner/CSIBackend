from django.contrib import admin
from django.urls import path, re_path
from patients import views
from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('patients.urls')),
    path('api/users/',  views.UserList.as_view()),
    path('api/users/<int:pk>/', views.users_detail),
    path('api/hello/', views.loginView),
]

urlpatterns = format_suffix_patterns(urlpatterns)