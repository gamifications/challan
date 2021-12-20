from django.shortcuts import redirect, render
from django.http import JsonResponse # , HttpResponse


from django.views import View
from django.contrib.auth.decorators import login_required



from .models import ChallanFile, Account
from .forms import AccountForm
from .pdf import GeneratePDF
# Create your views here.


@login_required
def home(request):
    if request.method == 'POST':
        print(request.POST)
        cfile = ChallanFile.objects.create(
            amount=request.POST['amount'],
            account_id = request.POST['acno'],
            cash_deposit= request.POST['denominations'],
        )
        pdf_gen = GeneratePDF(cfile, request.build_absolute_uri()[:-1])
        pdf_gen.generate()
        
        return redirect('/')


    context = {
        'files':ChallanFile.objects.order_by('-uploading_date')[:5],
        'accounts':[{'id': ac.id,'text': ac.name,'account':ac.ac_no} for ac in Account.objects.order_by('name')],
    }
    return render(request,'home.html',context)


class AccountView(View):
    def post(self,request):
        
        form = AccountForm(request.POST)
        if form.is_valid():
            item = form.save()
            message = {'status':'success', 'data':{'id':item.id,'text':item.name,'account':item.ac_no}}
        else:
            message = {'status':'failed', 'data':str(form.errors)}

        return JsonResponse(message)