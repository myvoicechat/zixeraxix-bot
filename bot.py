from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from openai import OpenAI
import os

# =========================
# ENV VARIABLES
# =========================

BOT_TOKEN = os.getenv("8689630119:AAGPluXAhhiOOoTusUjGx7klFMsGTa_jjho")
NVIDIA_API_KEY = os.getenv("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")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

BOT_NAME = "@Zixeraxix_bot"

# =========================
# BUTTON GRID
# =========================

keyboard = [
    [KeyboardButton("💬 Chat AI"), KeyboardButton("🧠 Ask Anything")],
    [KeyboardButton("🖼 Image Prompt"), KeyboardButton("💻 Coding Help")],
    [KeyboardButton("🎮 Game Idea"), KeyboardButton("📜 Shayari")],
    [KeyboardButton("👑 Owner"), KeyboardButton("ℹ️ Help")]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
👋 Welcome to {BOT_NAME}

🔥 Powerful AI Telegram Bot
⚡ Powered By NVIDIA AI

👑 Owner : Prince

✅ Features:
• AI Chat
• Coding Help
• Image Prompt
• Shayari
• Game Ideas
• Smart Replies

💎 Credit : {BOT_NAME}
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# =========================
# AI CHAT
# =========================

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    loading = await update.message.reply_text("🤖 Thinking...")

    try:

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a smart AI assistant.
Always reply stylishly.
Always add:
💎 Credit : {BOT_NAME}
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
            top_p=1,
            max_tokens=4096
        )

        response = completion.choices[0].message.content

        final_text = f"""
{response}

━━━━━━━━━━━━━━━
💎 Credit : {BOT_NAME}
"""

        await loading.edit_text(final_text)

    except Exception as e:
        await loading.edit_text(f"❌ Error:\n{e}")

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )

    print(f"{BOT_NAME} is running...")

    app.run_polling()

if __name__ == "__main__":
    main()
