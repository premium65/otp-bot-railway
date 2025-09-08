import os
from pyrogram import Client, filters
from pyrogram.types import Message
import zipfile

API_ID = int(os.environ.get("API_ID", 22815381))
API_HASH = os.environ.get("API_HASH", "de80983b057a7f8e22a88b8a83c21d20")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8250710501:AAHpkNhAh2pBgD8SF5Eb8Q7REH_Ide12h08")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply_text("✅ Railway Bot is ONLINE! 🚀\nSend me a .zip file to show the session files inside.")

@app.on_message(filters.document & filters.private)
def session_from_zip(client: Client, message: Message):
    doc = message.document
    if doc.file_name.endswith('.zip'):
        temp_zip = f"temp_{doc.file_name}"
        message.reply_text("⏬ Downloading your zip...")
        doc_path = client.download_media(message, file_name=temp_zip)
        try:
            filelist = []
            with zipfile.ZipFile(doc_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    filelist.append(file)
                    # If you want to display content, uncomment next lines:
                    # zip_ref.extract(file)
                    # with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    #     content = f.read(500)  # Show first 500 chars
                    #     message.reply_text(f"File: {file}\n\n{content}")
                    # os.remove(file)
            if filelist:
                msg = "🗂 Files found in your zip:\n\n"
                msg += "\n".join([f"- {name}" for name in filelist])
                message.reply_text(msg)
            else:
                message.reply_text("❌ No files found in the zip.")
        except Exception as e:
            message.reply_text(f"❌ Error reading zip: `{e}`")
        os.remove(doc_path)
    else:
        message.reply_text("Please send a .zip file containing your sessions.")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
