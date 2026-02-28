import os
from telegram.ext import ApplicationBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

print("FastMedia Bot running...")

app.run_polling()