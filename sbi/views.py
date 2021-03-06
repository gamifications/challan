from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


from .models import ChallanFile, Account, OtherBankChallanFile, OtherBankAccount, Depositor, Applicant
from .forms import AccountForm, OtherbankAccountForm
from .pdf import GeneratePDF, GenerateOtherBanksPDF

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('sbi_challan')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "500.html", {})

@method_decorator([login_required], name='dispatch')
class SBIBankView(View):

    def post(self, request, *args, **kwargs): 
        account = Account.objects.get(id=request.POST['acno'])       
        
        cheque= None
        if request.POST['chequeamount'] and request.POST['chequenumber']:
            cheque=[request.POST['chequeamount'], request.POST['chequenumber']]

        
        cfile = ChallanFile.objects.create(
            user=request.user,
            amount=int(request.POST['amount'])+ int(cheque[0]) if cheque else request.POST['amount'],
            # account_id = request.POST['acno'],
            name = account.name,
            cash_deposit= request.POST['denominations'],
        )
        depositor = Depositor.objects.filter(id=request.POST['depositor']).first()
        pdf_gen = GeneratePDF(cfile,account,cheque,depositor, request.build_absolute_uri()[:-1])
        pdf_gen.generate()
        messages.success(request, 'Challan generated successfully!')
        return redirect('sbi_challan')
    
    def get(self, request):
        context = {
            'files':ChallanFile.objects.filter(user=request.user).order_by('-uploading_date')[:5],
            'depositors': Depositor.objects.filter(user=request.user).order_by('name'),
            'accounts':[{
                'id': ac.id,
                'text': ac.name,
                'account':ac.ac_no,
                'branch':ac.branch,
                'telephone':ac.telephone,
                'pan':ac.pan,
                'email':ac.email,
            } for ac in Account.objects.filter(user=request.user).order_by('name')],
        }
        return render(request,'sbi/sbi.html',context)


@method_decorator([login_required], name='dispatch')
class DeleteChallanView(View):
    def post(self, request, *args, **kwargs):
        
        if request.POST.get('otherbank'):
            OtherBankChallanFile.objects.get(user=request.user,id=request.POST['challanid']).delete()
            url = 'otherbank_challan'
        else:
            ChallanFile.objects.get(user=request.user,id=request.POST['challanid']).delete()
            url = 'sbi_challan'
        
        messages.warning(request, 'Challan file deleted successfully!')
        return redirect(url)
        
@method_decorator([login_required], name='dispatch')
class addDepositorView(View):
    def post(self, request):
        if request.POST['name']:
            dep = Depositor.objects.create(user=request.user,name=request.POST['name'], adaar=request.POST['adaar'])
            return JsonResponse({'status':'success', 'id':dep.id, 'name':dep.name})
        
        return JsonResponse({'status':'failed', 'msg':'Name field is required.'})

@method_decorator([login_required], name='dispatch')
class deleteDepositorView(View):
    def delete(self, request, *args, **kwargs):
        query = Depositor.objects.get(user=request.user,pk=kwargs["pk"])
        query.delete()
        messages.warning(request, f'Depositor "{query.name}" deleted successfully!')
        return HttpResponse("Deleted!")
@method_decorator([login_required], name='dispatch')
class OtherBankView(View):

    def post(self, request):
        cheque= None
        if request.POST['chequenumber'] and request.POST['chequedate']:
            cheque=[request.POST['chequenumber'], request.POST['chequedate']]
        neft_rtgs = request.POST['neft_rtgs']
        account = OtherBankAccount.objects.get(user=request.user,id=request.POST['acno'])
        amt = request.POST['amount']
        bankcharge = request.POST.get('bankcharge',0)
        cfile = OtherBankChallanFile.objects.create(
            user=request.user,
            amount=amt,
            name=account.name
        )
        applicant = Applicant.objects.filter(user=request.user,id=request.POST['applicant']).first()
        pdf_gen = GenerateOtherBanksPDF(cfile,account,cheque,applicant,neft_rtgs, request.build_absolute_uri('/')[:-1])
        pdf_gen.generate(bankcharge)
        messages.success(request, 'Challan generated successfully!')
        return redirect('otherbank_challan')
    def get(self, request):
        context = {
            'applicants': Applicant.objects.filter(user=request.user),
            'files':OtherBankChallanFile.objects.filter(user=request.user).order_by('-uploading_date')[:5],
            'otherbank':True,
            'accounts':[{
                'id': ac.id,
                'text': ac.name,
                'account':ac.ac_no,
                'bank': ac.bank,
                'branch':ac.branch,
                'mobile':ac.mobile,
                'pan':ac.pan,
                'ifsc':ac.ifsc,
            } for ac in OtherBankAccount.objects.filter(user=request.user).order_by('name')],

            # 'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in OtherBankAccount.objects.filter(user=request.user).order_by('name')],
        }
        return render(request,'sbi/other.html',context)



@method_decorator([login_required], name='dispatch')
class AccountEditView(View):
    def post(self,request, *args, **kwargs):
        ac = Account.objects.get(user=request.user,pk=kwargs["pk"])
        ac.name = request.POST['name']

        ac.ac_no = request.POST['ac_no']
        ac.branch = request.POST['branch']
        ac.telephone = request.POST['telephone']
        ac.email = request.POST['email']
        ac.pan = request.POST['pan']

        ac.save()
        messages.success(request, f'Account "{ac.ac_no}" updated successfully!')
        return JsonResponse({'status':'success', 'data':[]})
    
    def delete(self, request, *args, **kwargs):
        if request.GET.get('ac') and request.GET['ac']=='other':
            query = OtherBankAccount.objects.get(user=request.user,pk=kwargs["pk"])
        else:
            query = Account.objects.get(user=request.user,pk=kwargs["pk"])
        query.delete()
        messages.warning(request, f'Account "{query.ac_no}" deleted successfully!')
        return HttpResponse("Deleted!")
        

@method_decorator([login_required], name='dispatch')
class AccountView(View):
    def post(self,request):
        form = AccountForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            message = {'status':'success', 'data':{
                'id':item.id,'text':item.name,'account':item.ac_no,
                'branch':item.branch,'telephone':item.telephone,
                'pan':item.pan,'email':item.email,}}
        else:
            message = {'status':'failed', 'data':str(form.errors)}
        
        return JsonResponse(message)


@method_decorator([login_required], name='dispatch')
class OtherbankAccountView(View):
    def post(self,request):
        form = OtherbankAccountForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            message = {'status':'success', 
                'data':{
                     'id': item.id,
                    'text': item.name,
                    'account':item.ac_no,
                    'bank': item.bank,
                    'branch':item.branch,
                    'mobile':item.mobile,
                    'pan':item.pan,
                    'ifsc':item.ifsc,
                }
            }
        else:
            message = {'status':'failed', 'data':str(form.errors)}
        return JsonResponse(message)


@method_decorator([login_required], name='dispatch')
class OtherbankAccountEditView(View):
    def post(self,request, *args, **kwargs):
        ac = OtherBankAccount.objects.get(user=request.user,pk=kwargs["pk"])
        ac.name = request.POST['name']

        ac.ac_no = request.POST['ac_no']
        ac.bank = request.POST['bank']
        ac.branch = request.POST['branch']
        ac.mobile = request.POST['mobile']
        ac.pan = request.POST['pan']
        ac.ifsc = request.POST['ifsc']
        ac.save()
        messages.success(request, f'Account "{ac.ac_no}" updated successfully!')
        return JsonResponse({'status':'success', 'data':[]})
class IFSCView(View):
    def post(self,request):
        import requests
        r = requests.get(f'https://bank-apis.justinclicks.com/API/V1/IFSC/{request.POST["ifsc"]}/')
        try:
            resp = r.json()
            message = {'status':'success', 'data':{'bank':resp['BANK'],'branch':resp['BRANCH'],'city': resp['CITY']}}
        except:
            message = {'status':'failed'}
        return JsonResponse(message)
        # return render(request, 'sbi/bank_details.html', {'bank': resp})


@method_decorator([login_required], name='dispatch')
class addApplicantView(View):
    def post(self, request):
        if request.POST['name']:
            dep = Applicant.objects.create(user = request.user,name=request.POST['name'], 
                address=request.POST['address'], account=request.POST['account'])
            return JsonResponse({'status':'success', 'id':dep.id, 'name':dep.name})
        return JsonResponse({'status':'failed', 'msg':'Name field is required.'})



@method_decorator([login_required], name='dispatch')
class deleteApplicantView(View):
    def delete(self, request, *args, **kwargs):
        query = Applicant.objects.get(user = request.user,pk=kwargs["pk"])
        query.delete()
        messages.warning(request, f'Applicant "{query.name}" deleted successfully!')
        return HttpResponse("Deleted!")