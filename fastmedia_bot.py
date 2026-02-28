import os
import asyncio
import subprocess
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

queue = asyncio.Queue()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 FastMedia Bot aktif.\nKirim link video.")


async def enqueue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Link diterima. Masuk antrian.")
    await queue.put((update, url))


async def worker():
    while True:

        update, url = await queue.get()

        msg = await update.message.reply_text("Memulai download...")

        uid = str(uuid.uuid4())
        filepath = f"{DOWNLOAD_DIR}/{uid}.mp4"

        try:

            cmd = [
                "yt-dlp",
                "--no-playlist",
                "-f",
                "bv*+ba/b",
                "--merge-output-format",
                "mp4",
                "--retries",
                "5",
                "--fragment-retries",
                "5",
                "--add-header",
                "User-Agent:Mozilla/5.0",
                "-o",
                filepath,
                url,
            ]

            subprocess.run(cmd)

            if not os.path.exists(filepath):
                await msg.edit_text("Download gagal.")
                queue.task_done()
                continue

            await msg.edit_text("Upload...")

            with open(filepath, "rb") as video:
                await update.message.reply_video(video)

            await msg.delete()

        except Exception:
            await update.message.reply_text("Terjadi error.")

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

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
    main()def main():

    app = ApplicationBuilder().token(TOKEN).post_init(start_worker).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enqueue))

    print("FastMedia Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()            try:
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
