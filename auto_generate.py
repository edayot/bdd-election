import pyodbc
import json
import random

# Connect to _Elections.accdb
path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"


try:
    conn.close()
except:
    pass

# Establish the connection
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')

cursor = conn.cursor()
query=f"""
DELETE FROM Bulletin
WHERE Bulletin.Id_election = 17
"""
cursor.execute(query)



cursor = conn.cursor()
query1 = "INSERT INTO Bulletin (Id_bulletin, Id_vote, Id_election, Id_bureaux) VALUES (?, ?, ?, ?)"


bureaux=[
    {"id":"57001","proba_sarkozy":0.4,"proba_hollande":0.5,"proba_blanc":0.1,"proba_nul":0.05},
    {"id":"57002","proba_sarkozy":0.8,"proba_hollande":0.1,"proba_blanc":0.05,"proba_nul":0.05},
    {"id":"57003","proba_sarkozy":0.1,"proba_hollande":0.1,"proba_blanc":0,"proba_nul":0.8},
    {"id":"57004","proba_sarkozy":0.5,"proba_hollande":0.5,"proba_blanc":0,"proba_nul":0},
    {"id":"57005","proba_sarkozy":0.5,"proba_hollande":0.5,"proba_blanc":0,"proba_nul":0},
    {"id":"57006","proba_sarkozy":0.5,"proba_hollande":0.5,"proba_blanc":0,"proba_nul":0},
    {"id":"57007","proba_sarkozy":0.2,"proba_hollande":0.7,"proba_blanc":0,"proba_nul":0.1},
    {"id":"57008","proba_sarkozy":0.1,"proba_hollande":0.7,"proba_blanc":0.99,"proba_nul":0.01},
    {"id":"57009","proba_sarkozy":0.5,"proba_hollande":0.5,"proba_blanc":0,"proba_nul":0}
]

cursor=conn.cursor()
query=f"""
SELECT ID FROM Toxicode
"""
cursor.execute(query)

bureaux_normaux=[{"id":bureau[0],"proba_sarkozy":0.48,"proba_hollande":0.52,"proba_blanc":0,"proba_nul":0} for bureau in cursor.fetchall()]

bureaux.extend(bureaux_normaux)




# sarkozy = 7, hollande = 8, blanc = 1 , nul = 2
k=0
k_prev="0"
for bureau in bureaux:
    k+=1
    k_str=str(k)
    if k_str[0]!=k_prev[0]:
        print(k, "bureaux traités sur", len(bureaux))
        k_prev=k_str

    for id_bulletin in range(100*k,100*k+100):
        choix = random.choices([7,8,1,2], weights=[bureau["proba_sarkozy"],bureau["proba_hollande"],bureau["proba_blanc"],bureau["proba_nul"]])[0]
        cursor.execute(query1, (id_bulletin, choix, 17, bureau["id"]))



conn.commit()
conn.close()






