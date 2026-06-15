from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# =====================
# CONFIG
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@FilmViralIndob"

# =====================
# DATABASE FILM
# =====================
FILM_DB = {
    "avengers": "https://t.me/link_avengers",
    "spiderman": "https://t.me/link_spiderman",
    "naruto": "https://t.me/link_naruto",
    "fast x": "https://t.me/link_fastx",
    "one piece": "https://t.me/link_onepiece"
}

# =====================
# CEK JOIN CHANNEL
# =====================
async def is_joined(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# =====================
# /START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 JOIN CHANNEL", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("✅ SUDAH JOIN", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "📢 Join channel dulu sebelum lanjut:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =====================
# CHECK JOIN BUTTON
# =====================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_joined(context, user_id):
        await query.message.reply_text(
            "🎬 Kirim judul film yang kamu mau:"
        )
    else:
        await query.message.reply_text(
            "❌ Kamu belum join channel!"
        )

# =====================
# HANDLE TEXT (FILM SEARCH)
# =====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in FILM_DB:
        await update.message.reply_text(
            f"🎬 LINK FILM:\n{FILM_DB[text]}"
        )
    else:
        await update.message.reply_text(
            "❌ Film tidak ditemukan!\nCoba ketik judul lain."
        )

# =====================
# MAIN APP
# =====================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
