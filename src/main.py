from datetime import datetime
from dotenv import load_dotenv
from serpapi import GoogleSearch
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



load_dotenv()
api_key = os.getenv("SERPAPI_KEY")
print(api_key)
historico_busca = "historico_busca_aero.xlsx"

def salvar_voo(voos):
    registros = []

    for voo in voos:
        flights = voo.get('flights', [{}])
        primeiro_voo = flights[0] if flights else{}

        registros.append({
            "Data_Consulta": datetime.today().strftime("%d/%m/%Y %H:%M"),
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
    else:
        df_final = df_novo

    df_final.to_excel(historico_busca, index=False)
    print(f"{len(registros)} voos salvos em {historico_busca}")

    return df_final

def buscar_passagens(origens, destino, data_ida, data_volta, valor_maximo, adultos=2):
    todos_voos = []

    for origem in origens:
        params = {
            "engine": "google_flights",
            "departure_id": origem,
            "arrival_id": destino,
            "outbound_date": data_ida,
            "return_date": data_volta,
            "currency": "BRL",
            "hl": "pt",
            "adults": adultos,
            "type": "1",
            "api_key": os.getenv("SERPAPI_KEY")
        }

        search = GoogleSearch(params)
        result = search.get_dict()
        print("Chaves retornadas:", result.keys())
        print("Resultado completo:", result)

        # atribui a váriavel os melhores valores segundo o google, com base em combinações, e caso não encontre, o código não é quebrado, pois retorna uma lista vazia.
        melhores = result.get("best_flights", [])
        outros = result.get("other_flights", [])
        print(f"Melhores: {len(melhores)} | Outros: {len(outros)}")

        # Adiciona a origem em cada voo para saber de onde veio
        for voo in melhores + outros:
            preco = voo.get('price', 0)


            link_geral = result.get("search_metadata", {}).get("google_flights_url")
            booking_token = voo.get("booking_token")
            link = None

            if booking_token:
                link =  f"https://www.google.com/travel/flights?tfs={booking_token}"
            else:
                link = link_geral or f"https://www.google.com/travel/flights?q={origem}-{destino}"

            if preco > 0 and preco <= valor_maximo:
                voo['origem_busca'] = origem
                voo['link'] = link
                todos_voos.append(voo)
                print(f"✅ Voo encontrado! {origem} → {destino} | R${preco} para {adultos} pessoas")
            else:
                print(f"❌ Voo acima do limite | R${preco} > R${valor_maximo}")

    # Salva no histórico
    if todos_voos:
        salvar_voo(todos_voos)
    else:
        print("Nenhum voo encontrado dentro do valor máximo")

    return todos_voos

def enviar_email(voos):
    if not voos:
        print('Nenhum voo para enviar')
        return

    melhor_voo = min(voos, key=lambda x: x.get('price', 0))
    preco = melhor_voo.get('price')
    origem = melhor_voo.get('origem_busca')
    duracao = melhor_voo.get('total_duration')
    link = melhor_voo.get('link')

    corpo = f"""
        <h2>Bom dia! Aqui está o melhor voo encontrado hoje:
        
        <p>
        🛫 Origem: {origem}
        🛬 Destino: POA
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

def main():
    print(f"\n🔍 Iniciando busca: {datetime.today().strftime('%d/%m/%Y %H:%M')}")
    voos = buscar_passagens(
        origens=["GRU", "CGH", "VCP"],
        destino="POA",
        data_ida="2026-09-04",
        data_volta="2026-09-07",
        valor_maximo=1500.00,
        adultos=2
    )
    enviar_email(voos)
    print(f"✅ Busca finalizada: {datetime.today().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()





