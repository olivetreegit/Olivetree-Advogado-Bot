import urllib.request
import re

# Link da versão consolidada para visualização (Texto Limpo)
url = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/1966-34509075'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

try:
    print("🏛️  Conectando ao Diário da República...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    print("🧹 Extraindo artigos...")
    # No DRE, o texto costuma estar em blocos de texto limpo
    # Vamos extrair tudo o que pareça texto legislativo
    texto_limpo = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    texto_limpo = re.sub(r'<[^>]*>', ' ', texto_limpo)
    texto_limpo = ' '.join(texto_limpo.split())
    
    # Formatação básica para o Bot
    texto_limpo = re.sub(r'(Artigo \d+[\.º\-A-Z]+)', r'\n\n\1', texto_limpo)
    
    if len(texto_limpo) > 50000:
        with open('codigo_civil_completo.txt', 'w', encoding='utf-8') as f:
            f.write(texto_limpo)
        print(f"✅ SUCESSO! Ficheiro criado com {len(texto_limpo)/1024:.2f} KB.")
    else:
        print("⚠️ O ficheiro parece pequeno demais. A tentar método alternativo...")
        
except Exception as e:
    print(f"❌ Erro: {e}")
