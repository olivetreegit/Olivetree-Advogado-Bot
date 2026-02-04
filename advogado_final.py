import subprocess, os, re

def consultar_ia(pergunta, contexto):
    prompt = (
        f"CONTEXTO LEGAL:\n{contexto}\n\n"
        f"PERGUNTA: {pergunta}\n\n"
        f"INSTRUÇÃO: Responde como um advogado amigo. 1. Usa emojis. 2. Faz um RESUMO curto. 3. Se o texto não for relevante, avisa com ⚠️."
    )
    try:
        process = subprocess.run(['ollama', 'run', 'kimi-k2.5:cloud', prompt], 
                               capture_output=True, text=True, encoding='utf-8', timeout=300)
        return process.stdout.strip()
    except Exception as e: return f"Erro na IA: {e}"

def buscar_contexto(ficheiro, busca):
    if not os.path.exists(ficheiro): 
        return f"Erro: O ficheiro {ficheiro} não foi encontrado!"
    
    with open(ficheiro, 'r', encoding='utf-8', errors='ignore') as f:
        conteudo = f.read()
    
    # Mapa de busca melhorado
    busca_norm = busca.lower()
    temas = {
        "férias": "Artigo 237", "patrão": "Deveres", "despedimento": "Artigo 340",
        "subsídio": "Artigo 262", "horas": "Artigo 226", "contrato": "Artigo 102",
        "aviso": "Artigo 400", "denúncia": "Artigo 400", "limite": "Artigo 27"
    }
    
    for chave, alvo in temas.items():
        if chave in busca_norm:
            match = re.search(rf"({alvo}.+?)(?=Artigo|\Z)", conteudo, re.IGNORECASE | re.DOTALL)
            if match: return match.group(1)[:4000]
            
    # Se não encontrar palavra-chave, faz busca simples por texto
    pos = conteudo.lower().find(busca_norm[:5])
    if pos != -1:
        return conteudo[max(0, pos-500):pos+3500]
    
    return conteudo[:4000]

def main():
    os.system('clear')
    print("🏛️  ADVOGADO VIRTUAL v19.6")
    print("1. 🏠 CIVIL | 2. 🚗 ESTRADA | 3. 💼 TRABALHO")
    op = input("\nEscolhe a área (1-3): ")
    
    biblioteca = {"1": "codigo_civil_completo.txt", "2": "codigo_estrada.txt", "3": "codigo_trabalho.txt"}
    f = biblioteca.get(op)
    
    if not f or not os.path.exists(f):
        print(f"⚠️ Erro: Ficheiro {f} não existe. Verifica a conversão do PDF.")
        return

    while True:
        duvida = input("\n🔍 Dúvida (ou 'sair'): ")
        if duvida.lower() in ['sair', 'exit', '']: break
        
        print("💡 O Kimi está a analisar...")
        ctx = buscar_contexto(f, duvida)
        print("-" * 50)
        print(consultar_ia(duvida, ctx))
        print("-" * 50)

if __name__ == "__main__": main()
