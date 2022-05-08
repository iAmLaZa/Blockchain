



import PyPDF2
import hashlib
def hashpdf(filename):

    pdfFileObj = open(filename, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # creating a page object
    pageObj = pdfReader.getPage(0)
    # extracting text from page
    print(pageObj.extractText())
    readable_hash = hashlib.sha256(pageObj.extractText().encode('utf-8')).hexdigest()
    # closing the pdf file object
    pdfFileObj.close()
    return readable_hash