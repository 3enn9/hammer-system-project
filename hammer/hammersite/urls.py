from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.send_code_view, name='send_code'),
    path('verify/', views.verify_code_view, name='verify_code'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/profile/', views.ProfileView.as_view(), name='api-profile'),
    path('api/send-code/', views.SendCodeView.as_view(), name='send_code'),
]
