import sqlite3
from datetime import datetime

def AddColumn():
    conn = sqlite3.connect('data_grabe.db')
    cursor = conn.execute(f'ALTER TABLE DataGrabe\
  ADD IsRead bit default 0;')
    conn.commit()
    conn.close()

def GetAll():
    conn = sqlite3.connect('data_grabe.db')
    cursor = conn.execute('SELECT * FROM DataGrabe')
    for row in cursor:
        print(row)
    conn.close()


def InsertData(f,b):
    conn = sqlite3.connect('data_grabe.db')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    conn.execute(f"INSERT INTO DataGrabe  \
      VALUES ('{f}', '{b}','{current_time}' )")
    conn.commit()
    conn.close()

def CreateTable():
     conn = sqlite3.connect('data_grabe.db')
     cursor = conn.execute(f'Create TABLE DataGrabe2(\
     FileName,BankName,CreateTime,IsRead bit default 0);')
     conn.commit()
     conn.close()
CreateTable()
# AddColumn()
# GetAll()
# InsertData("T","T")