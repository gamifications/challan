from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    ac_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    pan = models.CharField(max_length=100, blank=True)
    email= models.EmailField(blank=True)

class ChallanFile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True)
    cash_deposit = models.CharField(max_length=100) # '20,10, 500
    amount = models.FloatField(default=0)
    challanfile = models.FileField(upload_to = 'chalan/sbibank/')
    uploading_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.uploading_date}'
    
    def get_denominations(self):
        return self.cash_deposit.split(',')
class Depositor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    adaar = models.CharField(max_length=100)

class OtherBankAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ifsc = models.CharField(max_length=100)
    ac_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100, blank=True)
    pan = models.CharField(max_length=100, blank=True)

class OtherBankChallanFile(models.Model):
    # account = models.ForeignKey('OtherBankAccount', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    amount = models.FloatField(default=0)
    challanfile = models.FileField(upload_to = 'chalan/otherbank/')
    uploading_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.uploading_date}'

class Applicant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=300, blank=True)
    account = models.CharField(max_length=100, blank=True)