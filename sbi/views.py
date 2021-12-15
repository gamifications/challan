from django.shortcuts import redirect, render
from django.http import JsonResponse # , HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files import File
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from weasyprint import HTML
import inflect

from .models import ChallanFile, Account
from .forms import AccountForm
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
        
        amount_to_words = inflect.engine()
        context = {
            'file': cfile,
            'date': timezone.now(),
            'amount_in_words': amount_to_words.number_to_words(cfile.amount),
            'url': request.build_absolute_uri()[:-1] # strip last /
        }
        
        html = HTML(string=render_to_string('challan_template.html', context))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        cfile.challanfile.save(f'{cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))
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