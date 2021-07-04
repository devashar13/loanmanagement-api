from django.db.models.deletion import CASCADE, DO_NOTHING
from account.models import User
from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone

# Create your models here.
class Loan(models.Model):
    class LoanTypes(models.TextChoices):
        NEW = 'new', "NEW"
        APPROVED = 'approved', "APPROVED"
        REJECTED = 'rejected', "REJECTED"
        
    user = models.OneToOneField(User,on_delete=DO_NOTHING,related_name='user')
    created_by = models.OneToOneField(User,on_delete=DO_NOTHING,related_name='agent')
    loan_amount = models.DecimalField(max_digits=10,decimal_places=3)
    interest_rate = models.DecimalField(max_digits=10,decimal_places=3)
    loan_tenure = models.CharField(max_length=10)
    emi = models.DecimalField(max_digits=10,decimal_places=3) 
    created_at = models.DateTimeField(default=timezone.now)
    state = models.CharField(choices=LoanTypes.choices, default=LoanTypes.NEW, null=True, blank=True,max_length=20)
    approved_at = models.DateTimeField(blank=True,null=True)
    
