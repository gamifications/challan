from django import forms
from .models import Account, OtherBankAccount

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__' #('name', )


class OtherbankAccountForm(forms.ModelForm):
    class Meta:
        model = OtherBankAccount
        fields = '__all__' #('name', )
