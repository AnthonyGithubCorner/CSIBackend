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
    path('api/createusers/',  views.user_create),
    path('api/users/<int:pk>/', views.users_detail),
    # path('api/users/',  views.UserList.as_view()),

    #patient Dashboard
    path('api/patients/', views.PatientList.as_view()),
    path('api/createpatients/', views.patient_create),
    path('api/patients/<int:pk>/', views.patient_detail),
    path('api/patientprofile/', views.patient_profile),
    path('api/Modality/', views.ModalityResourceList.as_view()),
    path('token/obtain/', obtain_auth_token),

    #payer Dashboard
    path('api/payers/', views.PayerListCreate.as_view()),
    path('api/createpayers/', views.payer_create)

    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('test', views.home),
    # path('api/closest/<int:pk>/', views.closest),
]

urlpatterns = format_suffix_patterns(urlpatterns)