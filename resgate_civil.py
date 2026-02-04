import urllib.request
import os

fontes = [
    "https://raw.githubusercontent.com/centraldedados/codigos-portugueses/master/codigo-civil.md",
    "https://raw.githubusercontent.com/pvieira/codigos-portugueses-markdown/master/codigo-civil.md"
]

def baixar():
    for url in fontes:
        try:
            print(f"📡 A tentar fonte: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                conteudo = response.read()
                if len(conteudo) > 1000000: # Garantir que tem pelo menos 1MB
                    with open('codigo_civil_completo.txt', 'wb') as f:
                        f.write(conteudo)
                    print(f"✅ SUCESSO! Ficheiro gravado com {len(conteudo)/1024:.2f} KB")
                    return True
                else:
                    print("⚠️ Conteúdo recebido é demasiado pequeno, a tentar outra fonte...")
        except Exception as e:
            print(f"❌ Falha nesta fonte: {e}")
    return False

if __name__ == "__main__":
    if baixar():
        print("🚀 Tudo pronto. Podes correr o 'python3 advogado_final.py' agora.")
    else:
        print("💥 Todas as fontes falharam. Verifica a tua ligação à internet (ping google.com).")
