import os
import urllib.request
import urllib.parse
import json


# ============================================================
# CONFIGURAÇÃO DA NEWSAPI
# ============================================================

API_KEY = os.environ.get("NEWS_API_KEY")

if not API_KEY:
    raise Exception("NEWS_API_KEY não encontrada nas variáveis de ambiente.")


# ============================================================
# CATEGORIAS DE NOTÍCIAS
# ============================================================

CONSULTAS = {
    "engenheiro": '"data engineering" OR "data engineer" OR "data pipeline"',
    "cientista": '"data science" OR "artificial intelligence" OR "machine learning"',
    "analista": '"data analytics" OR "Power BI" OR "business intelligence"'
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
# COLETAR NOTÍCIAS DA NEWSAPI
# ============================================================

for profissao, consulta in CONSULTAS.items():

    print(f"Coletando: {profissao}")

    try:

        # ----------------------------------------------------
        # Monta os parâmetros da API
        # ----------------------------------------------------

        parametros = {
            "q": consulta,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": "5",
            "apiKey": API_KEY
        }


        # ----------------------------------------------------
        # Monta a URL
        # ----------------------------------------------------

        url = (
            "https://newsapi.org/v2/everything?"
            + urllib.parse.urlencode(parametros)
        )


        # ----------------------------------------------------
        # Faz a requisição
        # ----------------------------------------------------

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "DataNews-Hub"
            }
        )


        with urllib.request.urlopen(
            req,
            timeout=20
        ) as response:

            dados = json.loads(
                response.read().decode("utf-8")
            )


        # ----------------------------------------------------
        # Verifica resposta da API
        # ----------------------------------------------------

        if dados.get("status") != "ok":

            print(
                f"  ERRO DA NEWSAPI: "
                f"{dados.get('message', 'Erro desconhecido')}"
            )

            continue


        artigos = dados.get("articles", [])

        print(
            f"  Notícias encontradas: "
            f"{len(artigos)}"
        )


        # ----------------------------------------------------
        # Processa as notícias
        # ----------------------------------------------------

        for artigo in artigos:

            titulo = artigo.get(
                "title",
                "Sem título"
            )

            descricao = artigo.get(
                "description"
            )

            link = artigo.get(
                "url",
                "#"
            )

            fonte_dados = artigo.get(
                "source",
                {}
            )

            fonte = fonte_dados.get(
                "name",
                "Fonte desconhecida"
            )


            # ------------------------------------------------
            # Evita artigos sem título ou removidos
            # ------------------------------------------------

            if not titulo:
                continue

            if titulo == "[Removed]":
                continue


            # ------------------------------------------------
            # Classificação
            # ------------------------------------------------

            ferramenta_detectada, tag_detectada = (
                classificar_ferramenta(titulo)
            )


            # ------------------------------------------------
            # Resumo
            # ------------------------------------------------

            if descricao:

                resumo_pt = descricao

                resumo_en = descricao

            else:

                resumo_pt = (
                    "Leia a matéria completa "
                    "na fonte original."
                )

                resumo_en = (
                    "Read the full article "
                    "at the original source."
                )


            # ------------------------------------------------
            # Cria a notícia
            # ------------------------------------------------

            noticia = {

                "id": id_contador,

                "profissao": profissao,

                "ferramenta": ferramenta_detectada,

                "tag": tag_detectada,

                "titulo_pt": titulo,

                "titulo_en": titulo,

                "resumo_pt": resumo_pt,

                "resumo_en": resumo_en,

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
