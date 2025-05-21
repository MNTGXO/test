import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
CHANNELS = list(map(int, os.getenv("CHANNELS").split()))
REDIRECT_CHANNEL = int(os.getenv("REDIRECT_CHANNEL"))
REDIRECT_INVITE = os.getenv("REDIRECT_INVITE")
