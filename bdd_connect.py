

import pyodbc

# Connect to _Elections.accdb
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=_Elections.accdb;')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Elections")
for row in cursor.fetchall():
    print(row)
