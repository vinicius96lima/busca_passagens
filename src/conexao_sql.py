import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()
server = os.getenv('SERVER')
database = os.getenv('DATABASE')
uid = os.getenv('UID')
pwd = os.getenv('PWD')

def get_conexao():
    return pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={uid};"
    f"PWD={pwd};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)
