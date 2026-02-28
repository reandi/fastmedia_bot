import os
import uuid
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 FastMedia Bot aktif.\nKirim link video.")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    msg = await update.message.reply_text("Memulai download...")

    uid = str(uuid.uuid4())
    filepath = f"{DOWNLOAD_DIR}/{uid}.mp4"

    try:

        cmd = [
            "yt-dlp",
            "-f",
            "bv*+ba/b",
            "--merge-output-format",
            "mp4",
            "-o",
            filepath,
            url
        ]

        subprocess.run(cmd)

        if not os.path.exists(filepath):
            await msg.edit_text("Download gagal.")
            return

        await msg.edit_text("Upload video...")

        with open(filepath, "rb") as f:
            await update.message.reply_video(f)

        os.remove(filepath)

    except Exception:
        await msg.edit_text("Terjadi error.")


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
