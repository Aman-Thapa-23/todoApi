from distutils.log import Log
from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, AuthUserAPIView

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('user', AuthUserAPIView.as_view(), name="user"), 
    
]
