import os
import logging

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    MenuButtonWebApp, WebAppInfo
)
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not WEBAPP_URL or not WEBAPP_URL.startswith("https://"):
        await update.message.reply_text(
            "Mini App пока не настроен. Сначала добавь WEBAPP_URL "
            "(публичную HTTPS-ссылку на сайт) в переменные окружения."
        )
        return

    keyboard = [[InlineKeyboardButton(
        "🚀 Открыть NFT Gift Scanner",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    await update.message.reply_text(
        "🎁 NFT Gift Scanner\n\nОткрой мини-приложение кнопкой ниже.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def post_init(app: Application):
    if WEBAPP_URL and WEBAPP_URL.startswith("https://"):
        await app.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="NFT Scanner",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )


def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
