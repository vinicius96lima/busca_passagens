import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

def get_conexao():
    server = os.getenv('Server')
    database = os.getenv('Database')
    uid = os.getenv('Uid')
    pwd = os.getenv('Pwd')

    print("Server =", server)
    print("Database =", database)
    print("Uid =", uid)
    print("Pwd existe =", bool(pwd))

    return pyodbc.connect(
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={uid};"
        f"Pwd={pwd};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"

)
