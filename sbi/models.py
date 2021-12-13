from django.db import models

# Create your models here.
class Account(models.Model):
    branch = models.CharField(max_length=100)
    ac_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    pan = models.CharField(max_length=100)

class ChallanFile(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    cash_deposit = models.CharField(max_length=100) # '20,10, 500
    amount = models.FloatField(default=0)
    challanfile = models.FileField(upload_to = 'chalan/')
    uploading_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.uploading_date}'