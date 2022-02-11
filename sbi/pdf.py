from weasyprint import HTML
# import inflect
import json
from textwrap import wrap

from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings

from django.core.files import File

def amt_to_words(amt):
    import num2words
    amount_to_words = num2words.num2words(amt, lang='en_IN')

    # inf_engine = inflect.engine()
    # amount_to_words = inf_engine.number_to_words(amt)
    str_amt = ''
    for wrap_amt in wrap(f'{amount_to_words} Rupees Only',30):
        str_amt+= f'''
            <span style="border-bottom: 1px solid #000;">
                {wrap_amt.title()}
            </span><br>
        '''
    return str_amt
class GeneratePDF:
    def __init__(self, cfile,account,cheque, url):
        self.url = url 
        self.account = account
        self.cheque= cheque
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

        
        context = {
            'file': self.cfile,
            'account':self.account,
            'denom_total':self.cfile.amount - int(self.cheque[0]) if self.cheque else self.cfile.amount, # display denomiations total
            'cheque':self.cheque,
            'date': self.cfile.uploading_date, # timezone.now(),
            'amount_in_words': amt_to_words(self.cfile.amount),
            'url':  self.url, # strip last /
            'denoms': denoms,
        }
        
        html = HTML(string=render_to_string('pdf/sbi_challan_template.html', context))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        self.cfile.challanfile.save(f'{self.cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))

class GenerateOtherBanksPDF:
    def __init__(self, cfile, url):
        self.url = url 
        self.cfile = cfile

    def generate(self):
        context = {
            'file': self.cfile,
            'date': timezone.now(),
            'amount_in_words': amt_to_words(self.cfile.amount),
            'url':  self.url, # strip last /
        }
        
        html = HTML(string=render_to_string('pdf/otherbank_challan_template.html', context))
        html.write_pdf(f'{settings.MEDIA_ROOT}/output/challan.pdf')

        self.cfile.challanfile.save(f'{self.cfile.id}.pdf', File(open(f'{settings.MEDIA_ROOT}/output/challan.pdf','rb')))
