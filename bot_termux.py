#!/usr/bin/env python3
import telebot
import ollama
import os
from datetime import datetime

TOKEN = "COLA_TELEGRAM_TOKEN_AQUI"
MODEL = "llama3.2:1b"
bot = telebot.TeleBot(TOKEN)

def busca_leis(query):
    leis_dir = "./leis_txt"
    if not os.path.exists(leis_dir): return "Sem leis baixadas"
    
    resultados = []
    palavras = query.lower().split()
    
    for arquivo in os.listdir(leis_dir):
        if arquivo.endswith('.txt'):
            with open(f"{leis_dir}/{arquivo}", 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
                for palavra in palavras:
                    if palavra in conteudo.lower():
                        # Pega trecho relevante
                        inicio = conteudo.lower().find(palavra)
                        trecho = conteudo[inicio-200:inicio+800]
                        resultados.append(f"[{arquivo}] {trecho[:500]}...")
                        break
    
    return "

".join(resultados[:3]) if resultados else "Nada encontrado"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 LeiABot Termux online!
Pergunta sobre leis: 'prescrição', 'contrato', 'solar'...")

@bot.message_handler(func=lambda m: True)
def responder(m):
    query = m.text
    
    # Busca simples nos arquivos
    context = busca_leis(query)
    
    prompt = f"""LEIABOT Termux - Leis Portuguesas

CONTEXTO ENCONTRADO:
{context}

PERGUNTA: {query}

Responde CITANDO o contexto. Curto. Final: "⚠️ Não substitui advogado." """

    try:
        resp = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
        resposta = resp['message']['content']
        bot.reply_to(m, resposta)
        
        # Log
        with open("leiabot.log", "a") as f:
            f.write(f"{datetime.now()} | {query}
{resposta}
---
")
            
    except Exception as e:
        bot.reply_to(m, f"❌ Erro: {str(e)}")

print("🚀 LeiABot Termux pronto!")
bot.polling()
