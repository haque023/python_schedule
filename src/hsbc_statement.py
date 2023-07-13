import asyncio
import json
import os
import re
from datetime import datetime
import time

import aiohttp
import requests
from db import Is_File_Exists, Insert_FilRead
from helper import response


async def hsbc_all_files():
    dir_list = os.listdir("../r")
    for f in dir_list:
        if 'hsbc' in f and '.pdf' in f:
            if Is_File_Exists(f, "../r"):
                await hsbc_statement_save("../r/" + f)


async def hsbc_statement_save(file):
    extracted_text = response.extract_text_from_pdf(file)
    allText = ""
    for text in extracted_text:
        allText += text
    f = open("../r/hsbc.txt", "w")
    f.write(allText)
    f.close()
    pattern = '(\d{1,2} [A-Z]{1}[a-z]{2} \d{4}) ([A-Z0-9 \-+]+) ([\d{2}:\d{2}]+) (\d{1,2} [A-Z]{1}[a-z]{2} \d{4}) +([0-9,.-]+) +([0-9,.-]+)'
    result = re.findall(pattern, allText)
    pattern2 = 'Narrative (.+)'
    result2 = re.findall(pattern2, allText)
    result_ = re.findall(" +Account number +([0-9\-]+)", allText)
    if len(result_) <= 0:
        return

    account_no = result_[0].replace("-", "")
    opening = 0
    _list = []
    index = 0
    myJSON = []
    # print(index, len(result))
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
        elt0 = {}
        elt0["serial"] = index
        elt0["bankAccountId"] = 0
        elt0["dteDate"] = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")
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
            print(res["message"])
            if res["message"] == "Save Successfully":
                Insert_FilRead(file, "../r", True)
    time.sleep(10)
