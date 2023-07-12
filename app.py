import PyPDF2
import re


def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        return pdf_text


extracted_text = extract_text_from_pdf('r/hsbc.pdf')
allText = ""
for text in extracted_text:
    allText += text

f = open("w/hsbc.txt", "w")
f.write(allText)
f.close()