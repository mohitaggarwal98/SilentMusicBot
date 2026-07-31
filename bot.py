from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
import os
import yt_dlp

load_dotenv()

app = Client(
    "MohitMusicBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)


@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "👋 Hello! Welcome to Mohit Music Bot 🎵\n\n"
        "Use /help to see commands."
    )


@app.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text(
        "🎵 Commands:\n\n"
        "/start - Start bot\n"
        "/help - Help\n"
        "/play <song name> - Download song"
    )


@app.on_message(filters.command("play"))
async def play_cmd(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "🎵 Song name likho\nExample: /play Tum Hi Ho"
        )
        return

    song = " ".join(message.command[1:])

    msg = await message.reply_text(f"🔎 Searching: {song}")

    try:
        search = VideosSearch(song, limit=1)
        result = search.result()

        video = result["result"][0]
        url = video["link"]
        title = video["title"]

        await msg.edit_text(f"⬇️ Downloading:\n{title}")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        await message.reply_audio(
            audio=file,
            caption=f"🎵 {title}"
        )

        os.remove(file)

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


app.run()



