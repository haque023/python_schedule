from ebl_statement import ebl_all_files
from hsbc_statement import hsbc_all_files
from premire_bank_statement import premiere_all_files
import asyncio
async def start():
    await ebl_all_files()
    await hsbc_all_files()
    await premiere_all_files()

asyncio.run(start())
