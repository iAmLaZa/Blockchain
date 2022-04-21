from fpdf import FPDF
# pip install fpdf2

def CreateDiplomat(cordonnee_array):

# Create a pdf page L = landscape
    pdf = FPDF('L','mm','A4')

    # add a new Page
    pdf.add_page()
    # adding font
    pdf.add_font('sysfont','',r'Russo_One.ttf',uni=True)
    pdf.set_font('sysfont','',36)
    pdf.set_text_color(95, 97, 96)
    # the background      
    pdf.image(r'Certificate.jpg',x=0,y=0,w=297,h=210,type='',link='')
    j=0
    # madirsh 3liha
    pdf.cell(w=80,h=27,ln=True)
    #cordonee li yjo mn 3nd syed 
    for i in cordonnee_array:
        titles = ['Family Name : ','First Name : ','Age : ','Place of birth : ','Major : ','University : ']
        
        pdf.cell(30)
        pdf.cell(w=0,h=20,txt=titles[j] + i,ln=True)
        j+=1

    # creates a pdf file with name of the owner of the pdf
    pdf.output('{}_{}_file.pdf'.format(cordonnee_array[0],cordonnee_array[1]))

CreateDiplomat(['ibrahim','Ghozlane','21','Laghouat','SSI','USTHB'])