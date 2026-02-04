#!/usr/bin/env python3
import os, subprocess

def procura_lei(termo):
    # Procura em leis_txt/*.txt E leis_pdf/*.txt
    for pasta in ['leis_txt', 'leis_pdf']:
        if os.path.exists(pasta):
            cmd = f"grep -n -i '{termo}' {pasta}/*.txt 2>/dev/null | head -3"
            try:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if r.stdout.strip(): return r.stdout.strip()
            except: pass
    return f"❌ '{termo}' não encontrado"

print("🚀 ADVOGADO BOT 100% FUNCIONANDO!")
print("Testa: prescrição, condomínio, contrato, assembleia")
while True:
    query = input("
🔍 (sair): ")
    if query.lower() in ['sair', 'exit']: break
    print("
📜 " + procura_lei(query))
