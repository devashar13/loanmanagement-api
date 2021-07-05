
# from account.views import MyTokenObtainPairView
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login',UserLoginView.as_view() , name='login'),
    path('profile', UserProfileView.as_view(),name="profile"),
    path('register', UserRegistrationView.as_view(),name="register"),
    path('agentregister', AgentRegistrationView.as_view(),name="registeragent"),
    path('listusers', ListUsers.as_view(),name="listusers"),
    path('verifyagent', VerifyAgent.as_view(),name="verify-agent"),
    
    
    
]
