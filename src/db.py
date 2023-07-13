import sqlite3
from datetime import datetime
from sqlite3 import Error


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


def InsertData(f, b):
    conn = sqlite3.connect('data_grabe.db')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    conn.execute(f"INSERT INTO DataGrabe  \
      VALUES ('{f}', '{b}','{current_time}' )")
    conn.commit()
    conn.close()


def CreateTable():
    conn = sqlite3.connect('data_grabe.db')
    cursor = conn.execute(f'Create TABLE IF NOT EXISTS FileRead(\
     FileName,Directory,IsRead bit default 0);')
    conn.commit()
    conn.close()


def Insert_FilRead(f, l, r):
    print(f)
    conn = sqlite3.connect('data_grabe.db')
    conn.execute(f"INSERT INTO FileRead  \
      VALUES ('{f}', '{l}','{r}' )")
    conn.commit()
    conn.close()
    return True


def Is_File_Exists(f, l):
    try:
        conn = sqlite3.connect('data_grabe.db')
        cur = conn.cursor()
        cur.execute(f"Select * From FileRead where FileName='{f}' and Directory='{l}'")
        rows = cur.fetchall()
        for row in rows:
            return False
        conn.close()
        return True
    except Error as e:
        return False


def Read_All():
    try:
        conn = sqlite3.connect('data_grabe.db')
        cur = conn.cursor()
        cur.execute(f"Select * From FileRead")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        conn.close()
        return True

    except Error as e:
        return False


# Read_All()
CreateTable()
# AddColumn()
# GetAll()
# InsertData("T","T")
