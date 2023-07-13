from datetime import datetime
import re
from flaskr.services.helper import response
from decimal import Decimal
import json
from flaskr.database import database


def premiere_statement_save():
    db = database()
    extracted_text = response.extract_text_from_pdf('file/PremireBank.pdf')
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("file/PremireBank.txt", "w")
    f.write(allText)
    f.close()
    pattern = '([0-9,]+).(.{2}) ([0-9 \/A-Za-z;\-.\n:\%()\[\]&]+)(\d{2}\/\d{1,2}\/\d{4}) T  ([0-9,.]+)  ([0-9,.]+)'
    result = re.findall(pattern, allText)
    result_ = re.findall("([0-9 ]+) A\/C No [A-Z ]+:", allText)
    _opening = re.findall("Opening Balance +([0-9,.]+)", allText)

    account_no = result_[0]
    account_Id = db.get_bank_account_id_by_account_no(account_no)
    opening = float(_opening[0].replace(',', ''))
    _list = []
    for f in result:
        balance = float(f[0].replace(',', '')) + float("." + f[1].replace(',', ''))
        debit = float(f[4].replace(',', ''))
        credit = float(f[5].replace(',', ''))
        narration = f[2].replace('\n', ' ')
        date = datetime.strptime(f[3], '%d/%m/%Y').date().strftime('%m-%d-%Y')
        r = response(date, narration, debit, credit, balance)
        _list.append(r)
        db.add_statement_replica(
            body_object={'Serial': 1, 'BankAccountID': account_Id, 'date': date, 'Particulars': narration,
                         'InstrumentNo': '',
                         'debit': debit, 'credit': credit, 'balance': balance})

    return "Save Successfully"
    # jsonStr = json.dumps([obj.__dict__ for obj in list])
    # return jsonStr
