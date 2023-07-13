import PyPDF2


class response:
    def __init__(self, date, narration, debit, credit, balance):
        self.date = date
        self.narration = narration.replace('\n', ' ')
        self.debit = debit
        self.credit = credit
        self.balance = balance

    def extract_text_from_pdf(pdf_file):
        with open(pdf_file, 'rb') as pdf:
            reader = PyPDF2.PdfFileReader(pdf, strict=False)
            pdf_text = []
            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)
            return pdf_text
