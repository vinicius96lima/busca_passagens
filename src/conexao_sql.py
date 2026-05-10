import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

def get_conexao():
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    uid = os.getenv('UID')
    pwd = os.getenv('PWD')

    print("SERVER =", server)
    print("DATABASE =", database)
    print("UID =", uid)
    print("PWD existe =", bool(pwd))

    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"

)
