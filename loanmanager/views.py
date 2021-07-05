from django.shortcuts import render
from django.shortcuts import render
import decimal 
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
from django.utils import timezone

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
    permission_classes = (IsAuthenticated,)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    def get_queryset(self):
        
        user = self.request.user
        print(user)
        if user.is_staff == True:
            model = Loan.objects.all()
        elif user.is_staff == False and user.is_superuser == False:
            model = Loan.objects.filter(user = user)
        return model
class UpdateLoanState(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    
    def put(self, request): 
        verify_admin =  User.objects.filter(email = request.user).values("is_superuser","is_staff")
        if list(verify_admin)[0]['is_superuser'] == True :
            
            Loan.objects.filter(id = self.request.data['id']).update(
                state = self.request.data['state'],
                approved_at = timezone.now()
            )
            state = self.request.data['state']
            response = {
                    'success': 'true',
                    'message': f'Loan has been {state}',
                    
                    }
        

            return Response(response)
        return Response({"msg":"Route Blocked"})
            
            
class UpdateLoanState(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    
    def put(self, request): 
        verify_admin =  User.objects.filter(email = request.user).values("is_superuser","is_staff")
        if list(verify_admin)[0]['is_superuser'] == True :
            
            Loan.objects.filter(id = self.request.data['id']).update(
                state = self.request.data['state'],
                approved_at = timezone.now()
            )
            state = self.request.data['state']
            response = {
                    'success': 'true',
                    'message': f'Loan has been {state}',
                    
                    }
        

            return Response(response)
        return Response({"msg":"Route Blocked"})

class UpdateLoanState(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    
    def put(self, request): 
        verify_admin =  User.objects.filter(email = request.user).values("is_superuser","is_staff")
        if list(verify_admin)[0]['is_superuser'] == True :
            
            Loan.objects.filter(id = self.request.data['id']).update(
                state = self.request.data['state'],
                approved_at = timezone.now()
            )
            state = self.request.data['state']
            response = {
                    'success': 'true',
                    'message': f'Loan has been {state}',
                    
                    }
        

            return Response(response)
        return Response({"msg":"Route Blocked"})
class UpdateLoan(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = LoanSerializer
    def calc_emi(self,p,r,t):
        p = decimal.Decimal(p)
        r = decimal.Decimal(r)
        t = decimal.Decimal(t)
        r_month = (r /(12 * 100)) 
        t_month = t * (12) 
        # print(p,r,t,r_month,t_month)
        emi = (p * r_month * pow(1 + r_month, t_month)) / (pow(1 + r_month, t_month) - 1)
        rounded_emi = round(emi,3)
        # print(rounded_emi)
        return rounded_emi
    def put(self, request): 
        agent = request.user
        print(agent)
        if agent.is_staff== True and agent.is_superuser == False:
            print(Loan.objects.filter(id = request.data['id']).values('state').first())
            if Loan.objects.filter(id = request.data['id']).values('state').first()['state'] == "new":
                print(type(agent))
                print(type(str(Loan.objects.filter(id = request.data['id']).values('created_by__email').first()['created_by__email'])))
                if str(agent) == str(Loan.objects.filter(id = request.data['id']).values('created_by__email').first()['created_by__email']) :
                    
                    keys  = self.request.POST.keys()
                    if "state" in keys:
                        return Response({"msg":"You are not allowed to change the state"})
                    if 'amount' or "interest" or "tenure" in keys:
                        print("hi")
                        amount = request.data['amount'] if 'amount' in request.data else Loan.objects.filter(id = request.data['id']).values('loan_amount').first()['loan_amount']
                        interest = request.data['interest'] if 'interest' in request.data else Loan.objects.filter(id = request.data['id']).values('interest_rate').first()['interest_rate']
                        tenure = request.data['tenure'] if 'tenure' in request.data else Loan.objects.filter(id = request.data['id']).values('loan_tenure').first()['loan_tenure']
                        emi = decimal.Decimal(self.calc_emi(amount,interest,tenure))
                        print(type(emi))
                    

                    Loan.objects.filter(id = self.request.data['id']).update(
                        loan_amount = amount,
                        interest_rate = interest,
                        loan_tenure = tenure,
                        emi = emi,
                        created_at = timezone.now()
                    )
                    response = {
                            'success': 'true',
                            'message': f'Loan has been edited',
                            
                            }
                    return Response(response)
                    
                return Response({"msg":"You can not edit this loan as you did not create it"})
            return Response({"msg":"Loan has been approved cannot be edited"})
            

        return Response({"msg":"Route Blocked"})
            
            