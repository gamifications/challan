from weasyprint import HTML
import inflect
import json
from textwrap import wrap

from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings

from django.core.files import File

class GeneratePDF:
    def __init__(self, cfile, url):
        self.url = url 
        self.cfile = cfile

    def generate(self):
        denominations = json.loads(self.cfile.cash_deposit)
        denoms = []
        notes = [2000,500,200,100,50,20,10,5,1]
        for i,n in enumerate(denominations):
            item={
                'note':'Coins' if notes[i] == 1 else f'{notes[i]} x',
                'nums':'',
                'amt':''
            }
            if n: 
                item['nums']=n
                item['amt']=n*notes[i]

            denoms.append(item)

        inf_engine = inflect.engine()
        amount_to_words = inf_engine.number_to_words(self.cfile.amount)
        str_amt = ''
        for wrap_amt in wrap(f'{amount_to_words} Rupees Only',30):
            str_amt+= f'''
                <span style="border-bottom: 1px solid #000;">
                    {wrap_amt.title()}
                </span><br>
            '''
        context = {
            'file': self.cfile,
            'date': timezone.now(),
            'amount_in_words': str_amt,
            'url':  self.url, # strip last /
            'denoms': denoms,
        }
        
        html = HTML(string=render_to_string('challan_template.html', context))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        self.cfile.challanfile.save(f'{self.cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))

