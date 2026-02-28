import os
import asyncio
import subprocess
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

queue = asyncio.Queue()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 FastMedia Bot aktif!\n\n"
        "Kirim link YouTube / TikTok / Instagram."
    )


async def enqueue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("📥 Link diterima. Masuk antrian download...")

    await queue.put((update, context, url))


async def worker():

    while True:

        update, context, url = await queue.get()

        msg = await update.message.reply_text("⏳ Memulai download...")

        file_id = str(uuid.uuid4())

        filepath = f"{DOWNLOAD_DIR}/{file_id}.mp4"

        try:

            await msg.edit_text("⬇️ Download video...")

            cmd = [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio/best",
                "--merge-output-format",
                "mp4",
                "-o",
                filepath,
                url
            ]

            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if not os.path.exists(filepath):
                await msg.edit_text("❌ Download gagal.")
                queue.task_done()
                continue

            await msg.edit_text("⚙️ Compress video...")

            compressed = f"{DOWNLOAD_DIR}/{file_id}_c.mp4"

            compress_cmd = [
                "ffmpeg",
                "-i",
                filepath,
                "-vcodec",
                "libx264",
                "-crf",
                "28",
                "-preset",
                "fast",
                compressed
            ]

            subprocess.run(compress_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if os.path.exists(compressed):
                filepath = compressed

            size = os.path.getsize(filepath) / (1024 * 1024)

            await msg.edit_text(f"📤 Uploading ({size:.1f} MB)...")

            await update.message.reply_video(video=open(filepath, "rb"))

            await msg.delete()

        except Exception as e:

            await update.message.reply_text("❌ Error saat memproses.")

        finally:

            try:
                os.remove(filepath)
            except:
                pass

        queue.task_done()


async def start_worker(app):

    asyncio.create_task(worker())


def main():

    app = ApplicationBuilder().token(TOKEN).post_init(start_worker).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enqueue))

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
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
