import urllib.request
import re
import time

# URL que força a exibição de TODOS os artigos num só fôlego
url = 'https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=775&tabela=leis&so_artico=&pagina=1&ficha=1&nversao=&so_artico=S'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

def baixar():
    try:
        print("📡 Ligando aos servidores da PGDL...")
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            print("⏳ Descarregando dados (isto pode levar 30 segundos)...")
            # Lemos por partes para não sobrecarregar a conexão
            chunks = []
            while True:
                chunk = response.read(1024 * 64) # 64KB por vez
                if not chunk:
                    break
                chunks.append(chunk)
                print(f"📦 Recebidos {len(chunks) * 64} KB...", end="\r")
            
            html = b"".join(chunks).decode('iso-8859-1', errors='ignore')
        
        print("\n🧹 Processando texto...")
        
        # Limpeza profunda
        # Remove scripts, estilos e tags
        html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
        texto = re.sub(r'<[^>]*>', ' ', html)
        
        # Normalização
        texto = ' '.join(texto.split())
        
        # Formatação de Artigos (Garantir que cada um comece em linha nova)
        # O PGDL usa "Artigo 1.º", "Artigo 2.º-A", etc.
        texto = re.sub(r'(Artigo \d+[\.º\-A-Z\s]+)', r'\n\n\1', texto)

        with open('codigo_civil_completo.txt', 'w', encoding='utf-8') as f:
            f.write(texto)
        
        tamanho_final = len(texto) / 1024
        print(f"✅ FINALIZADO!")
        print(f"📊 Tamanho real no disco: {tamanho_final:.2f} KB")
        
        if tamanho_final < 1000:
            print("⚠️ ATENÇÃO: O ficheiro parece incompleto (menos de 1MB).")
            print("O site da PGDL pode estar a limitar a sessão. Tenta mudar de Wi-Fi para Dados Móveis.")
        else:
            print("🚀 SUCESSO! Agora tens o Código Civil em peso pesado.")

    except Exception as e:
        print(f"💥 Erro na extração: {e}")

if __name__ == "__main__":
    baixar()
