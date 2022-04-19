from django import forms
from .models import Account, OtherBankAccount

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)


class OtherbankAccountForm(forms.ModelForm):
    class Meta:
        model = OtherBankAccount
        exclude = ('user',)
