import feedparser
import json
import random
from datetime import datetime

# 1. PEGAR NOTÍCIAS DO STF/STJ (Dinâmico)
FONTES = {
    'stf': 'https://www.stf.jus.br/portal/rss/noticiasRss.asp',
    'stj': 'https://www.stj.jus.br/web/portal/feed/noticias'
}

feed_noticias = []

print("Buscando notícias frescas...")
for perfil, url in FONTES.items():
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:4]: # Pega as 4 mais recentes de cada
            texto_limpo = entry.summary.replace('<p>', '').replace('</p>', '').split('<br')[0]
            
            post = {
                "perfil": perfil, # stf ou stj
                "nome_autor": perfil.upper() + " Oficial",
                "texto": f"🚨 PLANTÃO: {entry.title}\n\n{texto_limpo}...",
                "data": datetime.now().isoformat(),
                "tipo": "noticia"
            }
            feed_noticias.append(post)
    except Exception as e:
        print(f"Erro no {perfil}: {e}")

# 2. LER AS LEIS FIXAS (Seu arquivo leis.json)
feed_leis = []
try:
    with open('leis.json', 'r', encoding='utf-8') as f:
        dados_leis = json.load(f)
        
        # Transforma o formato simples no formato completo do post
        for item in dados_leis:
            feed_leis.append({
                "perfil": item['perfil'],
                "texto": item['texto'],
                "data": datetime.now().isoformat(), # Data fictícia para ordenação
                "tipo": "lei"
            })
    print(f"Carregadas {len(feed_leis)} leis do banco de dados.")
except FileNotFoundError:
    print("Arquivo leis.json não encontrado. Usando apenas notícias.")

# 3. MISTURAR TUDO (O Algoritmo do Feed)
feed_final = feed_noticias + feed_leis
random.shuffle(feed_final) # Embaralha para não ficar repetitivo

# 4. SALVAR O ARQUIVO QUE O SITE LÊ (db.json)
with open('db.json', 'w', encoding='utf-8') as f:
    json.dump(feed_final, f, indent=2, ensure_ascii=False)

print("Feed atualizado e embaralhado com sucesso!")
