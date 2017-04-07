#NOTE: Uses lovely PDFDocument 3.1 by matthiask
#https://github.com/matthiask/pdfdocument
# ^ (A wrapper around the disgusting clunky reportlab)
import config, requests, sys, os
import pdfdocument.document as dc
from reportlab.lib.units import cm, mm
from flask import *
from io import BytesIO
from eduSource import NoteTaker
from cramBuilder import relevance

sys.path.insert(0, '.')

#setup the flask blueprin
main = Blueprint('main', __name__)

#our api endpoint route. users have parameter(s): origin, destination, one -> four
@main.route('/api', methods=['GET'])
def main_route():
    if request.method == 'GET':
        #get the user's topic by querystring 'topic'
        one = request.args.get('topic')

        #build the notetaker object, to do magic.
        topic = NoteTaker(one, 0, [], [])

        #get the relevant data.
        data = relevance(topic.takeNotes())

        #register pmncaecilia for our pdf to use.
        registerFont()

        #tailor the response so that it will display a pdf
        response = make_response(buildPDF(data,one,topic))
        response.headers['content-type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename="' + one + '.pdf"'

        return response
    return "ok"

def registerFont():
    #we have to acquire the absolute path of caecilia in order to register it..
    f = open(os.path.join(sys.path[0], 'OpenSans-Light.ttf'), 'r')

    #had to dig into pdfdocument source code to pull this off.
    dc.register_fonts_from_paths(regular=os.path.realpath(f.name),font_name='Open Sans')
    f.close() #close the filestream, don't need it anymore.

def buildPDF(data,head,topic):
    buffer = BytesIO()

    pdf = dc.PDFDocument(buffer)
    pdf.init_report()
    pdf.generate_style(font_name='Open Sans',font_size=10)
    pdf.address_head("Made with <3 @ HackOHI/O 2016")
    pdf.small("Learn More. Read Less-- " +\
        str(str(int(100 - (((len(data[0][1]) + len(data[1][1]) + len(data[2][1]) + len(data[3][1]) + len(data[4][1]) +\
        len(data[5][1]) + len(data[6][1]) + len(data[7][1])) / topic.size) * 100)))) + '%' + ' less.')
    pdf.h1(str(head))
    pdf.hr()
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    pdf.p(str(data[0][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[1][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[2][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[3][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[4][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[5][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[6][1]))
    pdf.spacer(height=0.3*cm)
    pdf.p(str(data[7][1]))
    pdf.spacer()
    pdf.h1("Potentially Relevant Links")
    pdf.hr()
    pdf.ul(topic.relevant)
    pdf.spacer()
    pdf.h1("Sources")
    pdf.ul(topic.sites)
    pdf.generate()
    pdf_out = buffer.getvalue()
    buffer.close()
    return pdf_out
