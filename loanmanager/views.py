from django.shortcuts import render
from django.shortcuts import render

from rest_framework import status
from rest_framework import response
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView,ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import LoanSerializer
from account.models import User
from .models import Loan

from django.http import HttpRequest
from rest_framework.generics import RetrieveAPIView,CreateAPIView



# Create your views here.
class CreateLoanView(CreateAPIView):

    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        agent = request.user
        data = request.data
        verify_agent =  User.objects.filter(email = agent).values("is_superuser","is_staff")
        print(verify_agent)
        if list(verify_agent)[0]['is_superuser'] == False and list(verify_agent)[0]['is_staff'] == True:
            user = User.objects.filter(email = data['user_email']).first()
            p = data['principal']
            r = data['interest']
            t = data['tenure']
            r_month = r / (12 * 100) 
            t_month = t * 12 
            emi = (p * r_month * pow(1 + r_month, t_month)) / (pow(1 + r_month, t_month) - 1)
            rounded_emi = round(emi,3)
            print(rounded_emi)
            # serialized_data = self.serializer_class(agent,emi,p,r,t,emi).data
            # serialized_data.is_valid(raise_exception=True)
            Loan.objects.create(
                user = user,
                created_by = agent,
                emi= emi,
                loan_amount= p,
                interest_rate= r,
                loan_tenure= t,
            )
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Loan Created Waiting Approval',
                
                }

            return Response(response, status=status_code)
        return Response({"msg":"Route Not allowed"})
    
class ListLoans(ListAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        model = Loan.objects.all()
        return model
class UpdateLoanState(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    
    def put(self, request): 
        verify_admin =  User.objects.filter(email = request.user).values("is_superuser","is_staff")
        if list(verify_admin)[0]['is_superuser'] == True :
            
            Loan.objects.filter(id = self.request.data['id']).update(
                state = self.request.data['state'] 
            )
            state = self.request.data['state']
            response = {
                    'success': 'true',
                    'message': f'Loan has been {state}',
                    
                    }
        

            return Response(response)
        return Response({"msg":"Route Blocked"})
            
            
        
