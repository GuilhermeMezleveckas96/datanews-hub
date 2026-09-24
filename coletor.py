```python
import urllib.request
import xml.etree.ElementTree as ET
import json


# ============================================================
# FEEDS RSS
# ============================================================

FEEDS = {
    "engenheiro": "https://news.google.com/rss/search?q=data+engineering&hl=en-US&gl=US&ceid=US:en",
    "cientista": "https://news.google.com/rss/search?q=data+science+artificial+intelligence&hl=en-US&gl=US&ceid=US:en",
    "analista": "https://news.google.com/rss/search?q=data+analytics+Power+BI&hl=en-US&gl=US&ceid=US:en"
}


# ============================================================
# BANCO DE NOTÍCIAS
# ============================================================

banco_noticias = []

id_contador = 1


print("==========================================")
print("     DATANEWS - COLETOR DE NOTÍCIAS")
print("==========================================")
print()


# ============================================================
# CLASSIFICAÇÃO DA FERRAMENTA
# ============================================================

def classificar_ferramenta(titulo):

    titulo_minusculo = titulo.lower()

    if "python" in titulo_minusculo:

        return "python", "Code"

    elif (
        "sql" in titulo_minusculo
        or "database" in titulo_minusculo
        or "banco de dados" in titulo_minusculo
    ):

        return "sql", "Query"

    elif (
        "power bi" in titulo_minusculo
        or "powerbi" in titulo_minusculo
        or "dashboard" in titulo_minusculo
    ):

        return "powerbi", "Analytics"

    elif (
        "openai" in titulo_minusculo
        or "chatgpt" in titulo_minusculo
        or "artificial intelligence" in titulo_minusculo
        or "ai" in titulo_minusculo
        or "inteligência artificial" in titulo_minusculo
    ):

        return "openai", "Artificial Intelligence"

    else:

        return "geral", "Atualidade"


# ============================================================
# COLETAR CADA FEED
# ============================================================

for profissao, url in FEEDS.items():

    print(f"Coletando: {profissao}")

    try:

        # ----------------------------------------------------
        # Faz a requisição
        # ----------------------------------------------------

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=20
        ) as response:

            xml_data = response.read()


        # ----------------------------------------------------
        # Interpreta o XML
        # ----------------------------------------------------

        root = ET.fromstring(xml_data)


        # ----------------------------------------------------
        # Encontra as notícias
        # ----------------------------------------------------

        itens = root.findall(".//item")

        print(
            f"  Notícias encontradas: {len(itens)}"
        )


        # Limita a 5 notícias por categoria

        for item in itens[:5]:

            # ------------------------------------------------
            # TÍTULO
            # ------------------------------------------------

            elemento_titulo = item.find("title")

            if (
                elemento_titulo is not None
                and elemento_titulo.text
            ):

                titulo = elemento_titulo.text.strip()

            else:

                titulo = "Sem título"


            # ------------------------------------------------
            # LINK
            # ------------------------------------------------

            elemento_link = item.find("link")

            if (
                elemento_link is not None
                and elemento_link.text
            ):

                link = elemento_link.text.strip()

            else:

                link = "#"


            # ------------------------------------------------
            # FONTE
            # ------------------------------------------------

            elemento_fonte = item.find("source")

            if (
                elemento_fonte is not None
                and elemento_fonte.text
            ):

                fonte = elemento_fonte.text.strip()

            else:

                fonte = "Google News"


            # ------------------------------------------------
            # CLASSIFICAÇÃO
            # ------------------------------------------------

            ferramenta_detectada, tag_detectada = (
                classificar_ferramenta(titulo)
            )


            # ------------------------------------------------
            # CRIA A NOTÍCIA
            # ------------------------------------------------

            noticia = {

                "id": id_contador,

                "profissao": profissao,

                "ferramenta": ferramenta_detectada,

                "tag": tag_detectada,

                "titulo_pt": titulo,

                "titulo_en": titulo,

                "resumo_pt":
                    "Leia a matéria completa na fonte original.",

                "resumo_en":
                    "Read the full article at the original source.",

                "fonte": fonte,

                "url": link
            }


            banco_noticias.append(noticia)

            id_contador += 1


    except Exception as e:

        print(
            f"  ERRO: {e}"
        )


    print()


# ============================================================
# SALVA O JSON
# ============================================================

with open(
    "noticias.json",
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        banco_noticias,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


# ============================================================
# RESULTADO
# ============================================================

print("==========================================")

print(
    f"Total de notícias coletadas: "
    f"{len(banco_noticias)}"
)

print("Arquivo noticias.json atualizado.")

print("==========================================")
```
