import pdfplumber
# pip install pdfplumber

def Extract(filename):

    with pdfplumber.open(filename) as pdf:
        first_page = pdf.pages[0]
        print(first_page.extract_text())


Extract('ibrahim_Ghozlane_file.pdf')
