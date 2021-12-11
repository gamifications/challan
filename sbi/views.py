from django.shortcuts import redirect, render
from weasyprint import HTML

from django.template.loader import render_to_string
from django.conf import settings
from django.core.files import File
from .models import ChallanFile

# Create your views here.
def home(request):
    if request.method == 'POST':
        html = HTML(string=render_to_string('challan_template.html', {'foo': 'bar'}))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        cfile = ChallanFile.objects.create(
                amount=100.50
            )

        cfile.challanfile.save(f'{cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))
        # template_data['output_files'].append(output_file)
        return redirect('/')
    
    return render(request,'home.html',{'files':ChallanFile.objects.order_by('-uploading_date')[:5]})
