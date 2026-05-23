import requests
import os
from dotenv import load_dotenv


load_dotenv()

def send_message_telegram(voos_poa, voos_vix):
    token = os.getenv('TELEGRANTOKEN')
    idchat = os.getenv('TELEGRANIDCHAT')
    try:
        mensagem = f'Bom dia, segue os melhores resultados de hoje:\n\n' \
                   f'{voos_poa}\n' \
                   f'{voos_vix}'
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, json={"chat_id": idchat,
                                 "text": mensagem,
                                 "parse_mode": "Markdown"})
        data = response.json()
        if not data['ok']:
            print(f"Erro Telegrma:{data['description']}")
        else:
            print("Mensagem enviada Telegram com sucesso")
    except requests.exceptions.ConnectionError():
        print("Sem Conexão")
    except requests.exceptions.Timeout:
        print("Timeout — Telegram demorou para responder")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
