import pyodbc

connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=prudens.database.windows.net;DATABASE=Prudens;UID=prudens;PWD=Test1234'
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
