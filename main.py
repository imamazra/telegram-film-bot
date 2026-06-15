from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@FilmViralindob"


# 🔥 CEK JOIN CHANNEL (FIXED)
async def is_joined(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🔥 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🔴 JOIN CHANNEL", url="https://t.me/FilmViralindob")],
        [InlineKeyboardButton("✅ SUDAH JOIN", callback_data="check")]
    ]

    await update.message.reply_text(
        "📢 Join channel dulu sebelum lanjut:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔥 CALLBACK CHECK
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_joined(context, user_id):
        await query.message.reply_text(
            "🎬 UNLOCK BERHASIL!\n👉 https://t.me/linkfilmkamu"
        )
    else:
        await query.message.reply_text(
            "❌ Kamu belum join channel!"
        )


# 🔥 APP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check))

app.run_polling()
