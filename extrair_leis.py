import urllib.request
import re

# Este URL aponta para o diploma 775 (Código Civil) em modo de exibição total
url = 'https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?artigo_id=&nid=775&tabela=leis&pagina=1&ficha=1&nversao=&so_artico='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print("📡 Acedendo ao articulado completo do Código Civil...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        # PGDL usa ISO-8859-1
        raw_html = response.read().decode('iso-8859-1', errors='ignore')
    
    print("🧹 Filtrando conteúdo (removendo menus e formulários)...")
    
    # Extrair apenas a parte que contém 'Artigo' para evitar o lixo do topo
    artigos_match = re.findall(r'Artigo.*', raw_html, re.DOTALL)
    if artigos_match:
        corpo_leis = artigos_match[0]
        # Limpeza de Tags
        clean_text = re.sub(r'<[^>]*>', ' ', corpo_leis)
        # Normalização de espaços
        clean_text = ' '.join(clean_text.split())
        # Formatação para o Bot: Garantir que cada Artigo começa numa linha nova
        clean_text = re.sub(r'(Artigo \d+\.º)', r'\n\1', clean_text)
        
        with open('codigo_civil_oficial.txt', 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        print(f"✅ SUCESSO! Ficheiro criado com {len(clean_text)} caracteres.")
        print(f"🔎 Verificação: 'Artigo 1366' presente? {'Sim' if 'Artigo 1366' in clean_text else 'Não'}")
    else:
        print("❌ Não foi possível encontrar o corpo da lei no HTML.")

except Exception as e:
    print(f"💥 Falha: {e}")
