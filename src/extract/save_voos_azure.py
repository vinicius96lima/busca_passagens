import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

#Contas de armazenametno/ rede/ chaves de acesso/ cadeia de conexao
url = os.getenv("AZUREARMAZENAMENTOURL")
container_name = os.getenv("AZURECONTAINERNAME")

def azure_load_xml(voos):
    arquivo = 'Relatorio_Busca_Voos.xlsx'
    voos.to_excel(arquivo, index=False)
    azure_conect_blob(arquivo)


def azure_conect_blob(arquivo):

    client = BlobServiceClient.from_connection_string(url)
    container_name = 'storagebuscavooxms'

    blob_client = client.get_blob_client(
        container=container_name,
        blob=arquivo
    )

    with open(arquivo, 'rb') as data:
        blob_client.upload_blob(
            data,
            overwrite=True
        )
    print('Arquivo Enviado para portal Azure com sucesso')
