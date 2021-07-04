
# from account.views import MyTokenObtainPairView
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('createloan',CreateLoanView.as_view() , name='create-loan'),
    path('listloans',ListLoans.as_view() , name='create-loan'),
    path('updateloanstate',UpdateLoanState.as_view() , name='update-state'),
    
    
    
]
