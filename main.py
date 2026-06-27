from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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
        [InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("✅ Saya Sudah Join", callback_data="check_join")]
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

            keyboard = [
                [InlineKeyboardButton("🟡 Klik Shopee", url="https://shopee.co.id")],
                [InlineKeyboardButton("✅ Konfirmasi", callback_data="confirm_ad")]
            ]

            await query.message.reply_text(
                "🔥 Join berhasil!\nSekarang klik tombol Shopee dulu sebelum lanjut 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await query.message.reply_text("❌ Kamu belum join channel!")

    # STEP 2: KONFIRMASI (tanpa tracking click ad karena Telegram tidak bisa detect URL click)
    elif query.data == "confirm_ad":

        keyboard = [
            [InlineKeyboardButton("🎬 Buka Film", url="https://t.me/linkfilmkamu")]
        ]

        await query.message.reply_text(
            "🎉 Akses dibuka",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ---------------- RUN BOT ----------------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
