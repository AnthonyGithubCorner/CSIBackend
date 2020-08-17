from django.contrib import admin
from django.urls import path, re_path
from main import views
from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/users/',  views.UserList.as_view()),
    path('api/users/<int:pk>/', views.users_detail),
    path('api/hello/', views.loginView),
    path('api/closest/<int:pk>/', views.closest),
    path('token/obtain/', obtain_auth_token),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('test', views.home),
]

urlpatterns = format_suffix_patterns(urlpatterns)