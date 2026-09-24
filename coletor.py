import urllib.request
import xml.etree.ElementTree as ET
import json

# Lista de feeds RSS focados em dados
FEEDS = {
    "engenheiro": "https://google.com",
    "cientista": "https://google.com",
    "analista": "https://google.com"
}

banco_noticias = []
id_contador = 1

print("Iniciando coleta com classificação de ferramentas...")

for profissao, url in FEEDS.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        # Coleta as principais notícias de cada feed
        for item in root.findall('.//item')[:5]:
            titulo = item.find('title').text if item.find('title') is not None else "Sem título"
            link = item.find('link').text if item.find('link') is not None else "#"
            fonte = item.find('source').text if item.find('source') is not None else "Google News"
            
            # Inteligência de Tags: Identifica a ferramenta pelo título da notícia
            titulo_minusculo = titulo.lower()
            ferramenta_detectada = "Geral"
            tag_detectada = "Atualidade"

            if "python" in titulo_minusculo:
                ferramenta_detectada = "python"
                tag_detectada = "Code"
            elif "sql" in titulo_minusculo or "banco de dados" in titulo_minusculo:
                ferramenta_detectada = "sql"
                tag_detectada = "Query"
            elif "power bi" in titulo_minusculo or "bi" in titulo_minusculo or "dashboard" in titulo_minusculo:
                ferramenta_detectada = "powerbi"
                tag_detectada = "Analytics"
            elif "openai" in titulo_minusculo or "chatgpt" in titulo_minusculo or "ia" in titulo_minusculo or "ai" in titulo_minusculo:
                ferramenta_detectada = "openai"
                tag_detectada = "Artificial Intelligence"

            noticia = {
                "id": id_contador,
                "profissao": profissao,
                "ferramenta": herramienta_detectada,
                "titulo_pt": titulo,
                "titulo_en": f"[EN] {titulo} (Official Source)",
                "resumo_pt": "Clique no link de leitura para conferir todos os detalhes técnicos diretamente no portal oficial desta notícia.",
                "resumo_en": "Click on the reading link to check all technical details directly on the official news portal.",
                "fonte": fonte,
                "link": link,
                "tag": tag_detectada
            }
            banco_noticias.append(noticia)
            id_contador += 1
            
    except Exception as e:
        print(f"Erro ao coletar do perfil {profissao}: {e}")

# Salva o arquivo JSON atualizado
with open('noticias.json', 'w', encoding='utf-8') as f:
    json.dump(banco_noticias, f, ensure_ascii=False, indent=4)

print(f"Sucesso! {len(banco_noticias)} notícias foram devidamente categorizadas.")
