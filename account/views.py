from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import AgentRegistrationSerializer, UserLoginSerializer, UserRegistrationSerializer, UserSerializer
from .models import User
from django.http import HttpRequest
from rest_framework.generics import RetrieveAPIView



class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)
class AgentRegistrationView(CreateAPIView):

    serializer_class = AgentRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Agent registered successfully Pending Verification from admin',
            }
        
        return Response(response, status=status_code)
class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    
    def get(self, request):
        
        try:
            
            user_profile = User.objects.get(email=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'id': user_profile.id,
                    'email': user_profile.email,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                }
            print(e)
        return Response(response, status=status_code)
    
class ListUsers(ListAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer
    
    def get(self, request):
        
        try:
            
            user_list = User.objects.all()
            serialized_data = self.serializer_class(user_list,many=True).data
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'users':serialized_data
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                }
            print(e)
        return Response(response, status=status_code)
    
    