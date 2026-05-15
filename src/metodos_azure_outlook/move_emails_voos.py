from src.services.connect_actions import connect_azure
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

def move_emails_voos(espera=10):
    headers = connect_azure()
    pasta_voos = os.getenv('IDFOLDERVOO')


    #Filtrar Assunto
    assunto_voo = "Melhor passagem"
    url = (
        "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
        f"?$top=50"
        f"&$filter=contains(subject,'{assunto_voo}')"
    )
    res = requests.get(url, headers=headers)
    emails = res.json()

    #Mover Emails
    body = {
        "destinationId": pasta_voos
    }

    if not emails['value']:
        print('Sem emails para serem movidos')
    else:
        time.sleep(espera)
        for email in emails["value"]:
            subject = email["subject"]
            destiantario = email["from"]["emailAddress"]["address"]
            received_date = email['receivedDateTime']
            message_id = email["id"]
            move_url = (f"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages/{message_id}/move")
            res = requests.post(move_url, headers=headers, json=body)
            print('Emails com voos movidos com sucesso')









