import os
import yt_dlp
import asyncio
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 FastMedia Bot aktif!\n\n"
        "Kirim link YouTube / TikTok / Instagram untuk download."
    )


def compress_video(input_file, output_file):
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "fast",
        "-acodec", "aac",
        "-b:a", "128k",
        output_file
    ]
    subprocess.run(cmd)


def download_media(url):

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "geo_bypass": True,
        "geo_bypass_country": "US",
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },
        "retries": 3,
        "fragment_retries": 3
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        if not filename.endswith(".mp4"):
            filename = filename.rsplit(".", 1)[0] + ".mp4"

    return filename


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    msg = await update.message.reply_text("⏳ Memulai download...")

    try:
        file_path = await asyncio.to_thread(download_media, url)

        size = os.path.getsize(file_path) / (1024 * 1024)

        # jika file terlalu besar untuk Telegram
        if size > 45:

            await msg.edit_text("📦 Mengompres video agar bisa dikirim...")

            compressed = file_path.replace(".mp4", "_compressed.mp4")

            await asyncio.to_thread(compress_video, file_path, compressed)

            file_path = compressed

        await msg.edit_text("📤 Mengirim video...")

        with open(file_path, "rb") as video:
            await update.message.reply_video(video)

        os.remove(file_path)

    except Exception as e:
        await msg.edit_text(f"❌ Gagal: {e}")


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_media)
    )

    app.add_error_handler(error)

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
