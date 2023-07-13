import re

from flaskr.database import database
from flaskr.services.helper import response
from decimal import Decimal
import json


def hsbc_statement_save():
    db = database()
    extracted_text = response.extract_text_from_pdf('file/hsbc.pdf')
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("file/hsbc.txt", "w")
    f.write(allText)
    f.close()
    pattern = '(\d{1,2} [A-Z]{1}[a-z]{2} \d{4}) ([A-Z0-9 \-+]+) ([\d{2}:\d{2}]+) (\d{1,2} [A-Z]{1}[a-z]{2} \d{4}) +([0-9,.-]+) +([0-9,.-]+)'
    result = re.findall(pattern, allText)
    pattern2 = 'Narrative (.+)'
    result2 = re.findall(pattern2, allText)
    result_ = re.findall(" +Account number +([0-9\-]+)", allText)
    account_no = result_[0].replace("-", "")
    account_Id = db.get_bank_account_id_by_account_no(account_no)
    opening = 0
    _list = []
    index = 0
    for f in result:
        balance = float(f[4].replace(',', ''))
        amount = float(f[5].replace(',', ''))
        credit = amount if amount > 0 else 0
        debit = amount if amount < 0 else 0
        narration = result2[index]
        index += 1
        date = f[3]
        r = response(date, narration, debit, credit, balance)
        _list.append(r)
        db.add_statement_replica(
            body_object={'Serial': 1, 'BankAccountID': account_Id, 'date': date, 'Particulars': narration,
                         'InstrumentNo': '',
                         'debit': debit, 'credit': credit, 'balance': balance})

    return "Save Successfully"
