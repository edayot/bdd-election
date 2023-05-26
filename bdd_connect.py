import pyodbc

# Connect to _Elections.accdb
path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"

# Establish the connection
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')

# Create a cursor object
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM Region")

# Fetch all rows
rows = cursor.fetchall()

# Process the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
