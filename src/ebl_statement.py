import os
import re
import time
from datetime import datetime
import aiohttp
from db import Insert_FilRead, Is_File_Exists
from helper import response


async def ebl_all_files():
    dir_list = os.listdir("C:/Users/Emdad-Pc/Desktop/python/r")
    for f in dir_list:
        if 'ebl' in f and '.pdf' in f:
            if Is_File_Exists(f, "../r"):
                await ebl_statement_save("C:/Users/Emdad-Pc/Desktop/python/r/" + f, f)


async def ebl_statement_save(file, name):
    # db = database()
    extracted_text = response.extract_text_from_pdf(file)
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("C:/Users/Emdad-Pc/Desktop/python/r/ebl.txt", "w")
    f.write(allText)
    f.close()

    pattern = '(\d{1,2}-[J,F,M,A,M,A,S,O,N,D][A-Z]{2}-\d{2}) +([a-zA-Z-_ &]+)(-?[\d,]+(?:\.\d+)?) +(-?[\d,]+(?:\.\d+)?)\n +([a-zA-Z_\-0-9 ]+)'
    result = re.findall(pattern, allText)
    pattern2 = '\/\/([0-9A-Z]+)'
    result2 = re.findall(pattern2, allText)

    account_pattern = " +Account Number : ([0-9]+)"
    result_ = re.findall(account_pattern, allText)
    if len(result_) <= 0:
        return

    account_no = result_[0]
    _list = []
    opening = 0
    last_balance = 0
    index = 0
    myJSON = []
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
        elt0 = {}
        elt0["serial"] = index
        elt0["bankAccountId"] = 0
        elt0["dteDate"] = datetime.strptime(date, "%d-%b-%y").strftime("%Y-%m-%d")
        elt0["particulars"] = ""
        elt0["accountNo"] = account_no
        elt0["instrumentNo"] = ""
        elt0["debit"] = debit
        elt0["credit"] = credit
        elt0["balance"] = balance
        elt0["insertBy"] = -100
        elt0["dteInsertDateTime"] = datetime.now().strftime("%Y-%m-%d")
        myJSON.append(elt0)

    async with aiohttp.ClientSession() as session:
        async with session.post("https://erp.ibos.io/fino/FinancialStatement/CreateTempDataEntry", json=myJSON) as resp:
            res = await resp.json()
            if res["message"] == "Save Successfully":
                Insert_FilRead(name, "../r", True)
            else:
                Insert_FilRead(name, "../r", False)

    time.sleep(6)
