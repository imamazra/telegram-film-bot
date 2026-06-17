from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

from database import user_state
from config import BOT_TOKEN, CHANNEL_USERNAME

# ---------------- CHECK JOIN ----------------
async def is_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔔 Join @FilmViralindob", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("✅ saya sudah join", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "Wajib join channel dulu sebelum lanjut 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- HANDLE CALLBACK ----------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # STEP 1: CEK JOIN
    if query.data == "check_join":
        if await is_joined(context, user_id):
            await query.message.reply_text(
                "🔥 Join berhasil!\n\nSekarang klik iklan dulu sebelum lanjut"
            )

            keyboard = [
    [InlineKeyboardButton("🔗 Klik Shopee", url="https%3A%2F%2Fs.shopee.co.id%2F8ATnWJ7fRR")],
    [InlineKeyboardButton("✅ Konfirmasi", callback_data="confirm_ad")]
]

            await query.message.reply_text(
                "Klik iklan terlebih dahulu 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.message.reply_text("❌ Kamu belum join channel!")

    # STEP 2: CLICK AD
    elif query.data == "click_ad":
        user_state[user_id] = {"ad_clicked": True}
        await query.message.reply_text("✔ Iklan tercatat, lanjut konfirmasi")

    # STEP 3: CONFIRM
    elif query.data == "confirm_ad":
        state = user_state.get(user_id, {})

        if state.get("ad_clicked"):
            await query.message.reply_text(
                "🎬 UNLOCK BERHASIL!\n👉 https://t.me/linkfilmkamu"
            )
        else:
            await query.message.reply_text("❌ Klik iklan dulu sebelum konfirmasi!")


# ---------------- RUN BOT ----------------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
