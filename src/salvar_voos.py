from datetime import datetime
import pandas as pd
import os
from insert_sql import inserir_base

historico_busca = r'C:\Users\Vinic\Desktop\Projeto_Busca_Aero\Projeto.xlsx'

def salvar_voo(top10):
    registros = []

    for voo in top10:
        flights = voo.get('flights', [{}])
        primeiro_voo = flights[0] if flights else{}

        registros.append({
            "Data_Consulta": datetime.today(),
            "Origem": voo.get("origem_busca"),
            "Destino": primeiro_voo.get("arrival_airport", {}).get("id"),
            "Companhia": primeiro_voo.get("airline"),
            "Preco_Total": voo.get("price"),
            "Duracao_Min": voo.get("total_duration"),
            "Link": voo.get("link")
        })
    df_novo = pd.DataFrame(registros)

    if os.path.exists(historico_busca):
        df_existente = pd.read_excel(historico_busca)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        df_final = df_final.drop_duplicates()
    else:
        df_final = df_novo

    df_final.to_excel(historico_busca, index=False)
    print(f"{len(registros)} voos salvos em {historico_busca}")

    return df_final