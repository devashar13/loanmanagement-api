from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db.models.query_utils import PathInfo
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from account.models import User
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
       class Meta:
        model = Loan
        fields = "__all__"
    
        #iddepart =  validated_data['iddepart']
        #idarrivee = validated_data['idarrivee']