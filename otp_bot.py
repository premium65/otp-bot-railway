import os
from pyrogram import Client, filters

# Get credentials from environment or use your hardcoded defaults
API_ID = int(os.environ.get("API_ID", 22815381))
API_HASH = os.environ.get("API_HASH", "de80983b057a7f8e22a88b8a83c21d20")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8250710501:AAHpkNhAh2pBgD8SF5Eb8Q7REH_Ide12h08")

# Create the bot client. No .session file needed for a bot.
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start handler
@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply_text("✅ Railway Bot is ONLINE! 🚀")

# Add more handlers here as you wish

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
