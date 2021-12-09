import json, os, sys, re
from weasyprint import HTML
import jinja2
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(os.path.expanduser("~"),"Desktop")
TEMPLATE_PATH = "templates" # "src/xcodepdf_package/templates"
    
def create_pdf():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(DIR_PATH))
    context= {'folder': f'{TEMPLATE_PATH}/', 'img_path':os.path.join('images')}        
    html_template = env.get_template(f"ticket.html")
    html = HTML(string=html_template.render(context))
    html.write_pdf('out.pdf')

if __name__ == '__main__':
    create_pdf()