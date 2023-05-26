import pyodbc
import json

# Connect to _Elections.accdb
path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"


try:
    conn.close()
except:
    pass

# Establish the connection
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')


cursor = conn.cursor()
query = "INSERT INTO Toxicode (type, ID, code_dpt, num_circ, code_reg , geometry) VALUES (?, ?, ?, ?, ?, ?)"

with open("france-circonscriptions-legislatives-2012.json") as f:
    d=json.load(f)


# Check if the table exists
table_name = "Toxicode"
try:
    cursor.execute("DROP TABLE " + table_name)
except:
    pass

create_table_query = """
CREATE TABLE Toxicode (
    type TEXT,
    ID TEXT PRIMARY KEY,
    code_dpt TEXT,
    num_circ TEXT,
    code_reg TEXT,
    geometry LONGCHAR
)
"""
cursor.execute(create_table_query)

conn.commit()


for feature in d["features"]:
    cursor.execute(query,
                   feature["type"], 
                   feature["properties"]["ID"], 
                   feature["properties"]["code_dpt"],
                   feature["properties"]["num_circ"],
                   feature["properties"]["code_reg"],
                   str(feature["geometry"]
                   )
    )


conn.commit()
conn.close()
