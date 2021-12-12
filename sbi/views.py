from django.shortcuts import redirect, render
from weasyprint import HTML

from django.template.loader import render_to_string
from django.conf import settings
from django.core.files import File
import inflect
from .models import ChallanFile, Account

# Create your views here.
def home(request):
    if request.method == 'POST':
        cfile = ChallanFile.objects.create(
            amount=100.50
        )
        context = {'file': cfile}
        amount_to_words = inflect.engine()
        context['amount_in_words'] = amount_to_words.number_to_words(cfile.amount)

        html = HTML(string=render_to_string('challan_template.html', context))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        cfile.challanfile.save(f'{cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))
        return redirect('/')
    
    return render(request,'home.html',{'files':ChallanFile.objects.order_by('-uploading_date')[:5]})
