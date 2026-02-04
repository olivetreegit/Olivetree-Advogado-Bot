import re
from bs4 import BeautifulSoup

def limpar_html():
    try:
        print("📖 A abrir cc.html com codificação Latin-1...")
        # Usamos latin-1 e 'ignore' para evitar que o script pare por caracteres estranhos
        with open('cc.html', 'r', encoding='iso-8859-1', errors='ignore') as f:
            html_content = f.read()
        
        print("🧹 A processar HTML (isto pode demorar em ficheiros de 8MB)...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove lixo
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        texto = soup.get_text(separator='\n')
        
        # Limpeza e Normalização
        linhas = [l.strip() for l in texto.splitlines() if l.strip()]
        texto_limpo = '\n'.join(linhas)
        
        # Garante que os Artigos fiquem isolados para a busca do Bot
        texto_limpo = re.sub(r'(?i)(Artigo\s+\d+)', r'\n\n\1', texto_limpo)

        with open('codigo_civil_completo.txt', 'w', encoding='utf-8') as f:
            f.write(texto_limpo)
            
        print(f"✅ SUCESSO!")
        print(f"📊 Ficheiro limpo: {len(texto_limpo)/1024:.2f} KB")

    except Exception as e:
        print(f"💥 Erro crítico: {e}")

if __name__ == "__main__":
    limpar_html()
