from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@FilmViralIndob"

# simple memory
user_state = {}

# ================= CHECK JOIN =================
async def is_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 JOIN CHANNEL",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
            )
        ],
        [
            InlineKeyboardButton("✅ SAYA SUDAH JOIN", callback_data="check_join")
        ]
    ]

    await update.message.reply_text(
        "📢 Wajib join channel dulu sebelum lanjut!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= CALLBACK HANDLER =================
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # STEP 1 - CHECK JOIN
    if query.data == "check_join":

        if await is_joined(context, user_id):

            user_state[user_id] = {"joined": True}

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🛍 Klik Shopee",
                        url="https://shopee.co.id/produk-kamu"
                    )
                ],
                [
                    InlineKeyboardButton("✅ Konfirmasi", callback_data="confirm_ad")
                ]
            ]

            await query.message.reply_text(
                "🔥 Join berhasil!\n\nSekarang klik Shopee dulu sebelum lanjut 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await query.message.reply_text("❌ Kamu belum join channel!")

    # STEP 2 - KONFIRMASI IKLAN
    elif query.data == "confirm_ad":

        state = user_state.get(user_id, {})

        if state.get("joined"):

            await query.message.reply_text(
                "🎬 UNLOCK BERHASIL!\n👉 https://t.me/linkfilmkamu"
            )

        else:
            await query.message.reply_text(
                "❌ Kamu belum menyelesaikan step sebelumnya!"
            )


# ================= RUN BOT =================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback))

app.run_polling()
