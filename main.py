import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, CHANNEL_USERNAME, SHOPEE_LINKS, FILM_VIDEOS
from database import user_state


# =========================
# CEK JOIN CHANNEL
# =========================
async def is_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("🔴 JOIN CHANNEL", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("✅ SUDAH JOIN", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "📢 Wajib join channel dulu sebelum lanjut:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# CHECK JOIN
# =========================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_joined(context, user_id):

        user_state[user_id] = "joined"

        keyboard = [
            [InlineKeyboardButton("🛒 KLIK SHOPEE", callback_data="shopee")]
        ]

        await query.message.reply_text(
            "✅ Kamu sudah join!\nLanjut klik tombol di bawah:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.message.reply_text("❌ Kamu belum join channel!")


# =========================
# SHOPEE STEP
# =========================
async def shopee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_state.get(user_id) != "joined":
        await query.message.reply_text("❌ Kamu belum valid join")
        return

    keyboard = [
        [InlineKeyboardButton("✅ KONFIRMASI", callback_data="confirm")]
    ]

    await query.message.reply_text(
        "📌 Klik Shopee dulu untuk lanjut:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# CONFIRM (FINAL UNLOCK)
# =========================
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    video = random.choice(FILM_VIDEOS)
    link = random.choice(SHOPEE_LINKS)

    await query.message.reply_text(
        f"🎬 VIDEO:\n{video}\n\n🛒 LINK:\n{link}"
    )


# =========================
# APP SETUP
# =========================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
app.add_handler(CallbackQueryHandler(shopee, pattern="shopee"))
app.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

app.run_polling()
