import os
import yt_dlp
import asyncio
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 FastMedia Bot aktif!\n\n"
        "Kirim link YouTube / TikTok / Instagram untuk download."
    )


def compress_video(input_file, output_file):
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vcodec",
        "libx264",
        "-crf",
        "28",
        "-preset",
        "fast",
        output_file,
    ]

    subprocess.run(cmd)


async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    status = await update.message.reply_text("⏳ Memulai download...")

    loop = asyncio.get_event_loop()

    filename = await loop.run_in_executor(None, download_video, url)

    await status.edit_text("📦 Memproses file...")

    filesize = os.path.getsize(filename)

    MAX_SIZE = 49 * 1024 * 1024

    if filesize > MAX_SIZE:

        compressed = filename + "_compressed.mp4"

        compress_video(filename, compressed)

        os.remove(filename)

        filename = compressed

    await status.edit_text("🚀 Upload ke Telegram...")

    await update.message.reply_video(video=open(filename, "rb"))

    os.remove(filename)

    await status.delete()


def download_video(url):

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_media)
    )

    app.add_error_handler(error)

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
