from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_vix(voos):
    if not voos:
        print('Nenhum voo para enviar')
        return

    voos_vix = [
        voo for voo in voos
        if voo.get('destino_busca') == 'VIX'
    ]

    if not voos_vix:
        return None

    melhor_voo_VIX = min(voos_vix, key=lambda x: x.get('price', 0))
    preco = melhor_voo_VIX.get('price')
    origem = melhor_voo_VIX.get('origem_busca')
    destino = melhor_voo_VIX.get('destino_busca')
    duracao = melhor_voo_VIX.get('total_duration')
    link = melhor_voo_VIX.get('link')
    print(f'voo poa {origem}, {destino}, {preco}')

    corpo = f"""
        <h2>Bom dia! Aqui está o melhor voo encontrado hoje:

        <p>
        🛫 Origem: {origem}
        🛬 Destino: {destino}
        💰 Preço: R${preco} para 2 pessoas
        ⏱️ Duração: {duracao} minutos
        </p>

        <p>
        <a href ="{link}">🔗 Clique aqui para ver o voo</a>
        </p>

        <p>📅 Data consulta: {datetime.today().strftime('%d/%m/%Y %H:%M')}</p>
        """

    msg = MIMEMultipart()
    msg.attach(MIMEText(corpo, 'html'))
    msg["FROM"] = os.getenv('EMAIL')
    msg['To'] = os.getenv('EMAIL_DESTINO')
    msg['Subject'] = f'Melhor passagem do dia | R$ {preco}'
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL'), os.getenv('APP_KEY'))
            server.sendmail(
                os.getenv('EMAIL'),
                os.getenv('EMAIL_DESTINO'),
                msg.as_string()
            )
            print('Email enviado com sucesso')
    except Exception as e:
        print(f'Erro ao enviar e-mail, {e}')