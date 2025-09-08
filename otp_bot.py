import os
import zipfile
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 22815381
API_HASH = "de80983b057a7f8e22a88b8a83c21d20"
BOT_TOKEN = "8250710501:AAHpkNhAh2pBgD8SF5Eb8Q7REH_Ide12h08"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("read_otp"))
async def ask_zip(client, message: Message):
    await message.reply("📥 Please send your ZIP file with sessions.")

@app.on_message(filters.document)
async def handle_zip(client, message: Message):
    file = message.document
    if not file.file_name.endswith(".zip"):
        await message.reply("❌ Please send a ZIP file!")
        return

    d = "sessions"
    os.makedirs(d, exist_ok=True)
    zip_path = await app.download_media(message, file_name=os.path.join(d, file.file_name))

    # Extract all session files
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(d)

    session_files = [f for f in os.listdir(d) if f.endswith(".session")]
    reply = []
    for sess in session_files:
        try:
            user_app = Client(os.path.join(d, sess), api_id=API_ID, api_hash=API_HASH, in_memory=True)
            await user_app.start()
            # Search for OTP in recent messages (you may want to change chat, e.g., a specific sender)
            async for m in user_app.get_chat_history("me", limit=30):
                if "otp" in m.text.lower():
                    reply.append(f"**User:** `{sess.replace('.session','')}`\n**OTP:** `{m.text}`")
                    break
            await user_app.stop()
        except Exception as e:
            reply.append(f"`{sess}` ❌ Error: {e}")

    if not reply:
        await message.reply("❌ No OTP found in any session.")
    else:
        for chunk in [reply[i:i+10] for i in range(0, len(reply), 10)]:
            await message.reply("\n\n".join(chunk))

if __name__ == "__main__":
    app.run()
