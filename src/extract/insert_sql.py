from src.services.conexao_sql import get_conexao


def inserir_base(df):
    conn_azure = get_conexao()
    cursor = conn_azure.cursor()
    cursor.fast_executemany = False

    sql = """
        INSERT INTO VOOS(
        DATA_CONSULTA,
        ORIGEM,
        DESTINO,
        PRECO_TOTAL,
        DURACAO,
        COMPANHIA,
        LINK                   
    )
        VALUES(?,?,?,?,?,?,?)
        """

    dados = list(df[[
        'Data_Consulta',
        'Origem',
        'Destino',
        'Preco_Total',
        'Duracao_Min',
        'Companhia',
        'Link'
    ]].itertuples(index=False, name=None))

    cursor.executemany(sql, dados)
    conn_azure.commit()
    cursor.close()
    conn_azure.close()

    return print(f'Dados inseridos com sucesso')