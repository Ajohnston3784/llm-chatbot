import os
from theme import get_theme

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

APP_TITLE = "LLM Chatbot Demo"
APP_ICON = "🤖"
APP_HEADER = "📚 AI Document Assistant"

theme = get_theme()
PRIMARY_COLOR = theme["PRIMARY_COLOR"]
SECONDARY_COLOR = theme["SECONDARY_COLOR"]
BACKGROUND_COLOR = theme["BACKGROUND_COLOR"]
CHAT_BG_COLOR = theme["CHAT_BG_COLOR"]
USER_MSG_BG = theme["USER_MSG_BG"]
BOT_MSG_BG = theme["BOT_MSG_BG"]
TEXT_COLOR = theme["TEXT_COLOR"]
INPUT_BG_COLOR = theme["INPUT_BG_COLOR"]

CHAT_HEIGHT = 550
