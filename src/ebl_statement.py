import re
from flaskr.services.helper import response
from flaskr.database import database


def ebl_statement_save():
    db = database()
    extracted_text = response.extract_text_from_pdf('file/ebl.pdf')
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("file/ebl.txt", "w")
    f.write(allText)
    f.close()

    pattern = '(\d{1,2}-[J,F,M,A,M,A,S,O,N,D][A-Z]{2}-\d{2}) +([a-zA-Z-_ &]+)(-?[\d,]+(?:\.\d+)?) +(-?[\d,]+(?:\.\d+)?)\n +([a-zA-Z_\-0-9 ]+)'
    result = re.findall(pattern, allText)
    pattern2 = '\/\/([0-9A-Z]+)'
    result2 = re.findall(pattern2, allText)

    account_pattern = " +Account Number : ([0-9]+)"
    result_ = re.findall(account_pattern, allText)
    account_no = result_[0]
    account_Id = db.get_bank_account_id_by_account_no(account_no)
    _list = []
    opening = 0
    last_balance = 0
    index = 0
    for f in result:
        last = ""
        if index != 0:
            last = result2[index - 1]
        index += 1
        balance = float(f[3].replace(',', ''))
        credit = f[2] if balance > last_balance else 0
        debit = f[2] if balance < last_balance else 0
        last_balance = balance
        date = f[0]
        narration = f[1].strip() + "\n" + f[4].strip() + "\n //" + last
        r = response(date, narration, debit, credit, balance)
        if index == 1:
            opening = balance
            continue
        _list.append(r)
        db.add_statement_replica(
            body_object={'Serial': 1, 'BankAccountID': account_Id, 'date': date, 'Particulars': narration, 'InstrumentNo': '',
                         'debit': debit, 'credit': credit, 'balance': balance})
    return "Save Successfully"
