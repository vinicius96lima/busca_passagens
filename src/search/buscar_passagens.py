from dotenv import load_dotenv
from serpapi import GoogleSearch
import os

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

def buscar_passagens(origens, destinos, data_ida, data_volta, valor_maximo, adultos=2):
    todos_voos = []

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

                elif preco <= valor_maximo * 1.80:
                    voo['origem_busca'] = origem
                    voo['destino_busca'] = destino
                    voo['link'] = link
                    todos_voos.append(voo)
                    print(f"✅ Voo encontrado 20 por cento acima do valor esperado! "
                          f"{origem} → {destino} | R${preco} para {adultos} pessoas")

                else:
                    print(f"❌ Voo acima do limite!"
                          f"{origem} → {destino} | R${preco} > R${valor_maximo}")

        todos_voos_poa = []
        preco_visto_poa = set()
        for voo in todos_voos:
            flights = voo.get('flights',[])
            preco = voo['price']
            if flights and preco:
                destino = flights[0]['arrival_airport']['id']
                if destino == 'POA' and preco not in preco_visto_poa:
                    preco_visto_poa.add(preco)
                    todos_voos_poa.append(voo)

        todos_voos_poa = sorted(todos_voos_poa, key=lambda x: x['price'])
        top10poa = todos_voos_poa[:10]

        todos_voos_vix = []
        preco_visto_vix = set()
        for voo in todos_voos:
            flights = voo.get('flights', [])
            preco = voo['price']
            if flights and preco:
                destino = flights[0]['arrival_airport']['id']
                if destino == 'VIX' and preco not in preco_visto_vix:
                    preco_visto_vix.add(preco)
                    todos_voos_vix.append(voo)

        todos_voos_vix = sorted(todos_voos_vix, key=lambda x: x['price'])
        top10vix = todos_voos_vix[:10]
        voos_unificados = top10poa + top10vix

        #Salva no histórico
        if voos_unificados:
           print('Voos Encontrados')
        else:
           print("Nenhum voo encontrado dentro do valor máximo")

    return voos_unificados