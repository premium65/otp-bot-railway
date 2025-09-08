import os
import zipfile
from pyrogram import Client, filters

API_ID = 22815381
API_HASH = "de80983b057a7f8e22a88b8a83c21d20"
BOT_TOKEN = "8250710501:AAHpkNhAh2pBgD8SF5Eb8Q7REH_Ide12h08"

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Railway Bot is ONLINE! 🚀\nSend me a .zip file with Telegram sessions to read OTP codes.")

@bot.on_message(filters.document)
async def handle_zip(client, message):
    if not message.document.file_name.endswith(".zip"):
        await message.reply("❌ Please send a .zip file only!")
        return

    # Download and extract the zip
    zip_dir = "sessions"
    os.makedirs(zip_dir, exist_ok=True)
    zip_path = await client.download_media(message, file_name=f"{zip_dir}/{message.document.file_name}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(zip_dir)

    session_files = [f for f in os.listdir(zip_dir) if f.endswith(".session")]
    if not session_files:
        await message.reply("❌ No .session files found in ZIP.")
        return

    # Process each session file
    results = []
    for session_file in session_files:
        session_path = os.path.join(zip_dir, session_file)
        try:
            user = Client(session_path, api_id=API_ID, api_hash=API_HASH, in_memory=True)
            await user.start()
            # Search for OTP in recent messages
            found = False
            async for msg in user.get_chat_history("me", limit=30):
                if msg.text and ("otp" in msg.text.lower() or "code" in msg.text.lower()):
                    results.append(
                        f"User: `{session_file.replace('.session','')}`\nOTP: `{msg.text}`"
                    )
                    found = True
                    break
            if not found:
                results.append(f"User: `{session_file.replace('.session','')}`\nOTP: Not found")
            await user.stop()
        except Exception as e:
            results.append(f"Session `{session_file}`: Error - {e}")

    # Reply results in chunks (Telegram limit)
    if results:
        for chunk in [results[i:i+10] for i in range(0, len(results), 10)]:
            await message.reply("\n\n".join(chunk))
    else:
        await message.reply("No OTPs found in any session.")

bot.run()
