import os
import pyodbc

def get_conexao():
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    uid = os.getenv('UID')
    pwd = os.getenv('PWD')

    print("SERVER =", server)
    print("DATABASE =", database)
    print("UID =", uid)
    print("PWD =", pwd)

    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={uid};"
        f"Pwd={pwd};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str)
