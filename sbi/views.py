from django.shortcuts import redirect, render
from django.http import JsonResponse # , HttpResponse


from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from .models import ChallanFile, Account
from .forms import AccountForm
from .pdf import GeneratePDF
# Create your views here.




# 




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
        
        return redirect('sbi_challan')
    
    def get(self, request):
        context = {
            'files':ChallanFile.objects.order_by('-uploading_date')[:5],
            'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in Account.objects.order_by('name')],
        }
        return render(request,'sbi/sbi.html',context)

@method_decorator([login_required], name='dispatch')
class OtherBankView(View):

    
    def get(self, request):
        context = {
            'files':ChallanFile.objects.order_by('-uploading_date')[:5],
            'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in Account.objects.order_by('name')],
        }
        return render(request,'sbi/other.html',context)



# @login_required
# def home(request):
#     if request.method == 'POST':
#         cfile = ChallanFile.objects.create(
#             amount=request.POST['amount'],
#             account_id = request.POST['acno'],
#             cash_deposit= request.POST['denominations'],
#         )
#         pdf_gen = GeneratePDF(cfile, request.build_absolute_uri()[:-1])
#         pdf_gen.generate()
        
#         return redirect('/')


    


class AccountView(View):
    def post(self,request):
        
        form = AccountForm(request.POST)
        if form.is_valid():
            item = form.save()
            message = {'status':'success', 'data':{'id':item.id,'text':item.name,'account':item.ac_no}}
        else:
            message = {'status':'failed', 'data':str(form.errors)}

        return JsonResponse(message)