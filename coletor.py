import urllib.request
import xml.etree.ElementTree as ET
import json

# Lista de feeds RSS de tecnologia/dados para testar
FEEDS = {
    "engenheiro": "https://google.com",
    "cientista": "https://google.com",
    "analista": "https://google.com"
}

banco_noticias = []
id_contador = 1

print("Iniciando coleta de notícias...")

for profissao, url in FEEDS.items():
    try:
        # Baixa o XML do feed RSS
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        # Parseia o XML
        root = ET.fromstring(xml_data)
        
        # Pega as 3 primeiras notícias de cada feed para o MVP
        for item in root.findall('.//item')[:3]:
            titulo = item.find('title').text if item.find('title') is not None else "Sem título"
            link = item.find('link').text if item.find('link') is not None else "#"
            fonte = item.find('source').text if item.find('source') is not None else "Google News"
            
            # Estrutura igualzinha ao que o nosso site espera receber
            noticia = {
                "id": id_contador,
                "profissao": profissao,
                "ferramenta": "Geral",
                "titulo_pt": titulo,
                "titulo_en": f"[EN] {titulo} (Click to read official source)", # Provisório até colocarmos tradução técnica
                "resumo_pt": "Clique no link abaixo para ler a matéria completa diretamente no portal oficial da fonte.",
                "resumo_en": "Click the link below to read the full article directly on the official source website.",
                "fonte": fonte,
                "link": link,
                "tag": "Atualidade"
            }
            banco_noticias.append(noticia)
            id_contador += 1
            
    except Exception as e:
        print(f"Erro ao coletar do perfil {profissao}: {e}")

# Salva todas as notícias reais encontradas em um arquivo JSON
with open('noticias.json', 'w', encoding='utf-8') as f:
    json.dump(banco_noticias, f, ensure_ascii=False, indent=4)

print(f"Sucesso! {len(banco_noticias)} notícias reais foram salvas no arquivo noticias.json.")
