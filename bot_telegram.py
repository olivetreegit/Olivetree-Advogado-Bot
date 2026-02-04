import os
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("TELEGRAM_TOKEN", "COLOQUE_O_TOKEN_AQUI")
MODELO = "kimi-k2.5:cloud"

FICHEIROS = {
    "🏠 CIVIL": "codigo_civil_completo.txt",
    "🚗 ESTRADA": "codigo_estrada.txt",
    "💼 TRABALHO": "codigo_trabalho.txt",
    "🚔 PENAL": "codigo_penal.txt"
}

user_choice = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🏠 CIVIL", "🚗 ESTRADA"], ["💼 TRABALHO", "🚔 PENAL"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🌳 *Olivetree Advogado v23.1* ⚖️\n\nSelecione a área jurídica:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    texto_recebido = update.message.text

    if texto_recebido in FICHEIROS:
        user_choice[user_id] = texto_recebido
        await update.message.reply_text(f"✅ Definido para: {texto_recebido}\nQual é a sua dúvida?")
        return

    if user_id in user_choice:
        area = user_choice[user_id]
        ficheiro = FICHEIROS[area]
        await update.message.reply_chat_action("typing")
        
        if not os.path.exists(ficheiro):
            await update.message.reply_text(f"❌ Erro: Ficheiro {ficheiro} não encontrado.")
            return

        try:
            with open(ficheiro, "r", encoding="utf-8") as f:
                # Lemos apenas uma parte para o contexto
                contexto_lei = f.read()[:12000] 

            prompt = (
                f"Tu és o Olivetree Advogado. Usa o {area} para responder: {contexto_lei}\n\n"
                f"Pergunta: {texto_recebido}\n\n"
                f"Responde de forma direta e curta."
            )
            
            process = subprocess.Popen(['ollama', 'run', MODELO, prompt], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            resposta = stdout if stdout else "Lamento, sem resposta."

            # --- SOLUÇÃO PARA O ERRO: CORTAR MENSAGEM ---
            if len(resposta) > 4000:
                resposta = resposta[:4000] + "\n\n...(Resposta encurtada por ser muito longa)..."
            
            await update.message.reply_text(resposta)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro: {e}")
    else:
        await update.message.reply_text("⚠️ Escolha uma área nos botões primeiro.")

if __name__ == '__main__':
    if TOKEN == "COLOQUE_O_TOKEN_AQUI":
        print("⚠️ ERRO: Token não configurado!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
        print("🚀 Olivetree Advogado ONLINE (v23.1 - Fix Long Message)")
        app.run_polling()
