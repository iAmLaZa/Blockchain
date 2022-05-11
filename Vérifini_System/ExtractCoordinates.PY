import pdfplumber
# pip install pdfplumber

def Extract(filename):

    with pdfplumber.open(filename) as pdf:
        first_page = pdf.pages[0]
        infos=first_page.extract_text().split(': ')
        infos=infos[1:]
        data = []
        for i in infos :
            if '\n' in i :
                data.append(i[:i.index('\n')])
            else :
                data.append(i)
        print(data)
        return data



