from dotenv import load_dotenv
from serpapi import GoogleSearch
import os
import pandas as pd
from salvar_voos import salvar_voo



load_dotenv()
api_key = os.getenv("SERPAPI_KEY")
print(api_key)


def buscar_passagens(origens, destinos, data_ida, data_volta, valor_maximo, adultos=2):
    todos_voos = []
    top10 = []

    for origem in origens:
        print(f'Iniciando Buscas com Origem, {origem}')

        for destino in destinos:
            print(f'Iniciando Busca com Destino, {destino}')

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

                if preco <= 0:
                    print('Preço inválido')

                elif preco <= valor_maximo:
                    voo['origem_busca'] = origem
                    voo['destino_busca'] = destino
                    voo['link'] = link
                    todos_voos.append(voo)
                    print(f"✅ Voo encontrado! "
                          f"{origem} → {destino} | R${preco} para {adultos} pessoas")

                elif preco <= valor_maximo * 1.20:
                    voo['origem_busca'] = origem
                    voo['destino_busca'] = destino
                    voo['link'] = link
                    todos_voos.append(voo)
                    print(f"✅ Voo encontrado 20 por cento acima do valor esperado! "
                          f"{origem} → {destino} | R${preco} para {adultos} pessoas")

                else:
                    print(f"❌ Voo acima do limite!"
                          f"{origem} → {destino} | R${preco} > R${valor_maximo}")




        todos_voos = sorted(todos_voos, key=lambda x: x['price'])
        top10 = todos_voos[:10]

        #Salva no histórico
        if top10:
           print('Voos Encontrados')
        else:
           print("Nenhum voo encontrado dentro do valor máximo")

    return top10