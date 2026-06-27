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
        [InlineKeyboardButton(
            "🔔 Join Channel",
            url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
        )],
        [InlineKeyboardButton("✅ Saya Sudah Join", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "Wajib join channel dulu sebelum lanjut 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- CALLBACK HANDLER ----------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # STEP 1: CEK JOIN
    if data == "check_join":

        if not await is_joined(context, user_id):
            keyboard = [
                [InlineKeyboardButton(
                    "🔔 Join Channel",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
                )],
                [InlineKeyboardButton("🔄 Cek Lagi", callback_data="check_join")]
            ]

            await query.message.reply_text(
                "❌ Kamu belum join channel",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        # kalau sudah join
        keyboard = [
            [InlineKeyboardButton(
                "🟡 Klik Shopee",
                url="https://bit.ly/4oNz7zi"
            )],
            [InlineKeyboardButton("✅ Saya Sudah Lihat", callback_data="confirm_ad")]
        ]

        await query.message.reply_text(
            "🔥 Join terverifikasi\nSekarang klik sponsor dulu sebelum lanjut 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # STEP 2: CONFIRM AD (tidak bisa tracking klik URL, hanya konfirmasi user)
    elif data == "confirm_ad":

        # simpan state sederhana
        user_state[user_id] = {
            "ad_confirmed": True
        }

        keyboard = [
            [InlineKeyboardButton(
                "🎬 Buka Film",
                url="https://t.me/linkfilmkamu"
            )]
        ]

        await query.message.reply_text(
            "🎉 Akses berhasil dibuka",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ---------------- RUN BOT ----------------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
