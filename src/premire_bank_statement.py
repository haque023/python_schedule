import os
import time
from datetime import datetime
import re
import aiohttp
from db import Is_File_Exists, Insert_FilRead
from helper import response



async def premiere_all_files():
    dir_list = os.listdir("C:/Users/Emdad-Pc/Desktop/python/r")
    for f in dir_list:
        if 'premiere' in f and '.pdf' in f:
            if Is_File_Exists(f, "../r"):
                await premiere_statement_save("C:/Users/Emdad-Pc/Desktop/python/r/" + f, f)


async def premiere_statement_save(file, name):
    extracted_text = response.extract_text_from_pdf(file)
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("C:/Users/Emdad-Pc/Desktop/python/r/PremireBank.txt", "w")
    f.write(allText)
    f.close()
    pattern = '([0-9,]+).(.{2}) ([0-9 \/A-Za-z;\-.\n:\%()\[\]&]+)(\d{2}\/\d{1,2}\/\d{4}) T  ([0-9,.]+)  ([0-9,.]+)'
    result = re.findall(pattern, allText)
    result_ = re.findall("([0-9 ]+) A\/C No [A-Z ]+:", allText)
    _opening = re.findall("Opening Balance +([0-9,.]+)", allText)

    if len(result_) <= 0:
        return
    account_no = result_[0]
    opening = float(_opening[0].replace(',', ''))
    _list = []
    myJSON = []
    index = 0
    for f in result:
        index += 1
        balance = float(f[0].replace(',', '')) + float("." + f[1].replace(',', ''))
        debit = float(f[4].replace(',', ''))
        credit = float(f[5].replace(',', ''))
        narration = f[2].replace('\n', ' ')
        date = datetime.strptime(f[3], '%d/%m/%Y').date().strftime('%m-%d-%Y')
        r = response(date, narration, debit, credit, balance)
        _list.append(r)
        elt0 = {}
        elt0["serial"] = index
        elt0["bankAccountId"] = 0
        elt0["dteDate"] = datetime.strptime(date, "%m-%d-%Y").strftime("%Y-%m-%d")
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

