import feedparser
import json
import os
from datetime import datetime

# Configuração das Fontes
FONTES = {
    'stf': 'https://www.stf.jus.br/portal/rss/noticiasRss.asp',
    'stj': 'https://www.stj.jus.br/web/portal/feed/noticias'
}

# Carregar banco de dados atual (se existir)
arquivo_db = 'db.json'
if os.path.exists(arquivo_db):
    with open(arquivo_db, 'r', encoding='utf-8') as f:
        try:
            posts = json.load(f)
        except:
            posts = []
else:
    posts = []

# Posts simulados de Leis (para encher o feed geral)
# Em um app real, isso viria de uma base de dados de leis
posts_leis = [
    { "perfil": "cp", "texto": "💡 Dica: No crime impossível (Art. 17), não se pune a tentativa por ineficácia absoluta do meio ou impropriedade absoluta do objeto.", "data": datetime.now().isoformat() },
    { "perfil": "cpc", "texto": "⚠️ Atenção: A contagem em dias úteis aplica-se apenas aos prazos processuais (Art. 219). Prazos materiais (decadência/prescrição) são dias corridos.", "data": datetime.now().isoformat() }
]

novos_posts = []

# BUSCA ATIVA (Scraping)
print("Iniciando varredura nos Tribunais...")

for perfil, url in FONTES.items():
    try:
        feed = feedparser.parse(url)
        # Pega as 3 notícias mais recentes
        for entry in feed.entries[:3]:
            # Limpa HTML básico do resumo
            texto_limpo = entry.summary.replace('<p>', '').replace('</p>', '').replace('<div>', '')
            
            post = {
                "perfil": perfil,
                "texto": f"📢 {entry.title}\n\n{texto_limpo[:200]}... [Ler mais no site]",
                "data": datetime.now().isoformat(),
                "link": entry.link
            }
            
            # Evita duplicatas (verifica se o título já existe)
            if not any(p['texto'].startswith(f"📢 {entry.title}") for p in posts):
                novos_posts.append(post)
                print(f"Nova notícia encontrada: {entry.title}")
                
    except Exception as e:
        print(f"Erro ao ler {perfil}: {e}")

# Adiciona posts de leis aleatórios para dar volume (simulação)
novos_posts.extend(posts_leis)

# Coloca os novos no topo
posts_atualizados = novos_posts + posts

# Mantém apenas os últimos 100 posts para o arquivo não ficar gigante
posts_atualizados = posts_atualizados[:100]

# Salva
with open(arquivo_db, 'w', encoding='utf-8') as f:
    json.dump(posts_atualizados, f, indent=2, ensure_ascii=False)

print("Banco de dados atualizado com sucesso.")
