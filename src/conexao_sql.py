import os
import pyodbc
import time

def get_conexao(max_tentativas=5, espera=20):
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    uid = os.getenv('UID')
    senhasql = os.getenv('SENHASQL')

    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={uid};"
        f"Pwd={senhasql};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    for tentativa in range(1, max_tentativas + 1):
        try:
            print(f'Tentativa {tentativa} de conexão...')
            conn = pyodbc.connect(conn_str)
            print("✅ Conexão com Azure SQL realizada!")
            return conn

        except Exception as e:
            print(f"❌ Erro na tentativa {tentativa}: {e}")

            if tentativa < max_tentativas:
                print(f"⏳ Aguardando {espera} segundos...")
                time.sleep(espera)
            else:
                print("🚨 Todas as tentativas falharam.")
                raise
