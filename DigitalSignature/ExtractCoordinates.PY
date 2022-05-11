import pdfplumber
# pip install pdfplumber

def Extract(filename):
    l= []
    with pdfplumber.open(filename) as pdf:
        first_page = pdf.pages[0]
        for i in first_page.extract_text().split('\n'):
            l.append(i.split(' : ')[1])
        return l    #l[0]= nom ,l[1]= prenom ,l[2] = matricule , l[3] = birthday , l[4] = place , l[5] = major
                    #l[6]= mention ,l[7] = university

