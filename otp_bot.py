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
    message.reply_text("✅ Railway Bot is ONLINE! 🚀\n\nSend me a .zip file to read OTP.")

@app.on_message(filters.document & filters.private)
def otp_from_zip(client: Client, message: Message):
    doc = message.document
    if doc.file_name.endswith('.zip'):
        temp_zip = f"temp_{doc.file_name}"
        message.reply_text("⏬ Downloading your zip...")
        doc_path = client.download_media(message, file_name=temp_zip)
        otp_found = False
        try:
            with zipfile.ZipFile(doc_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith('.txt'):
                        zip_ref.extract(file)
                        with open(file, 'r') as f:
                            otp_content = f.read().strip()
                        message.reply_text(f"🔑 OTP Content from `{file}`:\n\n`{otp_content}`", parse_mode="markdown")
                        otp_found = True
                        os.remove(file)
                        break
            if not otp_found:
                message.reply_text("❌ No .txt file found in the zip.")
        except Exception as e:
            message.reply_text(f"❌ Error extracting OTP: `{e}`")
        os.remove(doc_path)
    else:
        message.reply_text("Please send a .zip file containing the OTP.")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
