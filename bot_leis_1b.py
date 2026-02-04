#!/usr/bin/env python3
import telebot
import chromadb
from chromadb.utils import embedding_functions
import ollama
import fitz
import os
from datetime import datetime

TOKEN = "COLA_TELEGRAM_TOKEN_AQUI"
MODEL = "llama3.2:1b"
bot = telebot.TeleBot(TOKEN)

# RAG setup
client = chromadb.PersistentClient(path="./leis_db")
ef = embedding_functions.OllamaEmbeddingFunction(model_name=MODEL)
try:
    collection = client.get_collection("leis_pt")
except:
    collection = client.create_collection("leis_pt", embedding_function=ef)

def index_leis_rapido():
    count = len(collection.get()['ids'])
    if count > 0:
        print(f"✅ {count} leis já indexadas")
        return
    
    print("📥 Indexando leis...")
    leis_dir = "./leis_pdfs"
    if not os.path.exists(leis_dir):
        print("⚠️  Baixa leis primeiro:")
        print("mkdir leis_pdfs && cd leis_pdfs && wget https://diariodarepublica.pt/dr/legislacao-consolidada/codigo_civil/20231228/1/s1.pdf")
        return
    
    for pdf in os.listdir(leis_dir)[:3]:  # Só 3 PDFs teste
        if pdf.endswith('.pdf'):
            try:
                doc = fitz.open(f"{leis_dir}/{pdf}")
                texto = ""
                for page in doc: 
                    texto += page.get_text()
                chunks = [texto[i:i+3000] for i in range(0, len(texto), 3000)]
                
                collection.add(
                    documents=chunks,
                    metadatas=[{"fonte": pdf}] * len(chunks),
                    ids=[f"{pdf}_{i}" for i in range(len(chunks))]
                )
                print(f"✅ {pdf}")
            except Exception as e:
                print(f"❌ {pdf}: {e}")
    print("🎉 Indexação completa!")

index_leis_rapido()

@bot.message_handler(func=lambda m: True)
def responder_leis(m):
    query = m.text
    
    results = collection.query(query_texts=[query], n_results=2)
    context = "NENHUM DOCUMENTO ENCONTRADO"
    
    if results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            fonte = results['metadatas'][0][i]['fonte']
            context = f"📄 [{fonte}]:
{doc[:800]}...
"
            break  # Só 1 melhor contexto pro 1B
    
    prompt = f"""LEIABOT - Leis Portuguesas

CONTEXTO:
{context}

PERGUNTA: {query}

RESPOSTA (curta, cita fonte):
"""
    
    try:
        resp = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
        resposta = resp['message']['content'] + "

⚠️ Não é aconselhamento jurídico. Consulta advogado."
        
        # Log
        with open("leiabot.log", "a") as f:
            f.write(f"{datetime.now()} | {m.from_user.username}: {query}
{resposta}
---
")
        
        bot.reply_to(m, resposta)
    except Exception as e:
        bot.reply_to(m, f"❌ Erro: {str(e)}")

print(f"🚀 LeiABot 1B online! Envia /start no Telegram")
bot.polling()
