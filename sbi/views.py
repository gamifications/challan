from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


from .models import ChallanFile, Account, OtherBankChallanFile, OtherBankAccount
from .forms import AccountForm, OtherbankAccountForm
from .pdf import GeneratePDF, GenerateOtherBanksPDF

@method_decorator([login_required], name='dispatch')
class SBIBankView(View):

    def post(self, request, *args, **kwargs):        
        cfile = ChallanFile.objects.create(
            amount=request.POST['amount'],
            account_id = request.POST['acno'],
            cash_deposit= request.POST['denominations'],
        )
        pdf_gen = GeneratePDF(cfile, request.build_absolute_uri()[:-1])
        pdf_gen.generate()
        messages.success(request, 'Challan generated successfully!')
        return redirect('sbi_challan')
    
    def get(self, request):
        context = {
            'files':ChallanFile.objects.order_by('-uploading_date')[:5],
            'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in Account.objects.order_by('name')],
        }
        return render(request,'sbi/sbi.html',context)

@method_decorator([login_required], name='dispatch')
class OtherBankView(View):

    def post(self, request):
        amt = request.POST['amount']
        cfile = OtherBankChallanFile.objects.create(
            amount=amt,
        )
        pdf_gen = GenerateOtherBanksPDF(cfile, request.build_absolute_uri('/')[:-1])
        pdf_gen.generate()
        messages.success(request, 'Challan generated successfully!')
        return redirect('otherbank_challan')
    def get(self, request):
        context = {
            'files':OtherBankChallanFile.objects.order_by('-uploading_date')[:5],
            'otherbank':True,
            'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in OtherBankAccount.objects.order_by('name')],
        }
        return render(request,'sbi/other.html',context)


class AccountView(View):
    def post(self,request):
        
        form = AccountForm(request.POST)
        if form.is_valid():
            item = form.save()
            message = {'status':'success', 'data':{'id':item.id,'text':item.name,'account':item.ac_no}}
        else:
            message = {'status':'failed', 'data':str(form.errors)}

        return JsonResponse(message)




class OtherbankAccountView(View):
    def post(self,request):
        
        form = OtherbankAccountForm(request.POST)
        if form.is_valid():
            item = form.save()
            message = {'status':'success', 'data':{'id':item.id,'text':item.name,'account':item.ac_no}}
        else:
            message = {'status':'failed', 'data':str(form.errors)}

        return JsonResponse(message)

class IFSCView(View):
    def post(self,request):
        import requests
        r = requests.get(f'https://bank-apis.justinclicks.com/API/V1/IFSC/{request.POST["ifsc"]}/')
        try:
            resp = r.json()
        except:
            resp = None
        return render(request, 'sbi/bank_details.html', {'bank': resp})