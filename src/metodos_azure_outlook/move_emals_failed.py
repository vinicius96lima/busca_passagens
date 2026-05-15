from src.services.conexao_outlook import connect_azure
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

def move_emails_failed(espera=10):
    headers = connect_azure()
    pasta_failed = os.getenv('IDFOLDERLOGS')

    #Filtrar Assunto
    assunto_failed = 'Run failed'
    url = (
        "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
        f"?$top=50"
        f"&$filter=contains(subject,'{assunto_failed}')"
    )
    res = requests.get(url, headers=headers)
    emails = res.json()

    #Mover Emails
    body = {
        "destinationId": pasta_failed
    }

    if not emails['value']:
        print('Sem emails de falha para serem movidos')
    else:
        time.sleep(espera)
        for email in emails["value"]:
            subject = email["subject"]
            destiantario = email["from"]["emailAddress"]["address"]
            received_date = email['receivedDateTime']
            message_id = email["id"]
            move_url = (f"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages/{message_id}/move")
            res = requests.post(move_url, headers=headers, json=body)
            print('Emails de falhas movidos com sucesso')











