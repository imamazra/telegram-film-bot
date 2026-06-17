from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import random

from config import BOT_TOKEN, CHANNEL_USERNAME, SHOPEE_LINKS, FILM_LINKS

# =========================
# USER STATE (simple memory)
# =========================
user_state = {}

# =========================
# CHECK USER JOIN CHANNEL
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
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🔔 join @FilmViralindob",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ saya sudah join",
                callback_data="check_join"
            )
        ]
    ]

    await update.message.reply_text(
        "📢 Wajib join channel dulu sebelum lanjut 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# CALLBACK HANDLER
# =========================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # =====================
    # STEP 1: CHECK JOIN
    # =====================
    if data == "check_join":

        if await is_joined(context, user_id):
            user_state[user_id] = {"joined": True, "ad_clicked": False}

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔗 Klik Shopee",
                        url=random.choice(SHOPEE_LINKS)
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Konfirmasi",
                        callback_data="confirm_ad"
                    )
                ]
            ]

            await query.message.reply_text(
                "🔥 Join berhasil!\n\n"
                "Sekarang klik iklan dulu sebelum lanjut 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await query.message.reply_text(
                "❌ Kamu belum join channel!\nSilakan join dulu."
            )

    # =====================
    # STEP 2: CONFIRM
    # =====================
    elif data == "confirm_ad":

        state = user_state.get(user_id, {})

        if not state.get("joined"):
            await query.message.reply_text("❌ Kamu belum join channel!")
            return

        # OPTIONAL: kalau mau paksa klik iklan (simulasi tracking)
        state["ad_clicked"] = True
        user_state[user_id] = state

        # ambil film random
        film_link = random.choice(FILM_LINKS)

        await query.message.reply_text(
            "🎬 UNLOCK BERHASIL!\n"
            f"👉 {film_link}"
        )


# =========================
# RUN BOT
# =========================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
