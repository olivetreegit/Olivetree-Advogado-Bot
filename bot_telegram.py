import subprocess, os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Tenta carregar o token de forma segura
TOKEN = os.getenv("TELEGRAM_TOKEN", "COLOQUE_O_TOKEN_AQUI")
MODELO = "kimi-k2.5:cloud"

user_choice = {}

# ... (resto do código que já tínhamos) ...

if __name__ == '__main__':
    if TOKEN == "COLOQUE_O_TOKEN_AQUI":
        print("⚠️ Erro: Token não configurado! Usa: export TELEGRAM_TOKEN=teu_token")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
        print("🚀 Bot @Olivetree_Advogado_bot ONLINE!")
        app.run_polling()
