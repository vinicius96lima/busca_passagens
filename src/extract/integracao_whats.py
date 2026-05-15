from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from dotenv import load_dotenv

load_dotenv()

def send_message(send_whats_poa, send_whats_vix):
    account = os.getenv('ACCOUNT')
    token = os.getenv('TOKEN')
    num_from = os.getenv('NUMFROM')
    num_to = os.getenv('NUMTO')
    if not send_whats_poa and send_whats_vix:
        return
    else:
        notificacao_poa = send_whats_poa
        notificacao_vix = send_whats_vix
        account_sid = account
        auth_token = token

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=f'whatsapp:{num_from}',
                body=f"""Bom dia, Segue os melhores valores:
                        POA: {notificacao_poa}'
                        VIX: {notificacao_vix}'
                        """,
                to=f'whatsapp:{num_to}'
            )
            print('Mensagem enviada com sucesso!')
            return True
        except TwilioRestException as e:
            print("ERRO TWILIO")
            print(e)
            return False
