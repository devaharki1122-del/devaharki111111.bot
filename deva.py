# ================== 🤖 DEV AI BOT FULL ==================
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus
import json, os, datetime, openai, asyncio

# ================== ⚙️ CONFIG ==================
BOT_TOKEN = "8251863494:AAFzqYQsIYscVGtwbsnFxiklRc4vfJx_Ywg"
OPENAI_KEY = "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"
ADMIN_ID = 8186735286

CHANNELS = ["@chanaly_boot","@team_988","@my_d4ily"]
DATA_FILE = "data.json"

openai.api_key = OPENAI_KEY
# ==============================================

# ================== 📦 DATA ==================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,"w") as f:
        json.dump({"vvip":[],"free":{}}, f)

def load():
    with open(DATA_FILE) as f:
        return json.load(f)

def save(d):
    with open(DATA_FILE,"w") as f:
        json.dump(d,f,indent=2)
# =============================================

# ================== 🔒 FORCE JOIN ==================
async def is_member(bot, user_id):
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(ch, user_id)
            if m.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                return False
        except:
            return False
    return True
# ==============================================

# ================== ⏱ FREE LIMIT ==================
def reset_free(data, uid):
    today = str(datetime.date.today())
    if uid not in data["free"] or data["free"][uid]["date"] != today:
        data["free"][uid] = {"date": today, "count": 0}
# ==============================================

# ================== 🚀 START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    if not await is_member(context.bot, u.id):
        kb = [
            [InlineKeyboardButton("📢 جەنال 1", url="https://t.me/chanaly_boot")],
            [InlineKeyboardButton("📢 جەنال 2", url="https://t.me/team_988")],
            [InlineKeyboardButton("📢 جەنال 3", url="https://t.me/my_d4ily")],
            [InlineKeyboardButton("✅ پشکنین", callback_data="check")]
        ]
        await update.message.reply_text("🚫 سەرەتا Join بکە", reply_markup=InlineKeyboardMarkup(kb))
        return

    kb = [
        [InlineKeyboardButton("🆓 فری", callback_data="free")],
        [InlineKeyboardButton("👑 VVIP", callback_data="buy")]
    ]
    await update.message.reply_text("👋 بەخێربێیت بۆ AI BOT 🤖", reply_markup=InlineKeyboardMarkup(kb))
# ==============================================

# ================== 🔘 BUTTONS ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "check":
        await q.edit_message_text("✅ سەرکەوتوو")

    elif q.data == "free":
        await q.edit_message_text("🆓 5 جار ڕۆژانە")

    elif q.data == "buy":
        await q.edit_message_text("👑 بۆ کرین → پەیوەندی بکە @Deva_harki")
# ==============================================

# ================== 🤖 AI CHAT ==================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    text = update.message.text
    data = load()

    # VVIP = unlimited
    if int(uid) not in data["vvip"]:
        reset_free(data, uid)
        if data["free"][uid]["count"] >= 5:
            kb = [[InlineKeyboardButton("👑 بۆ کرین", callback_data="buy")]]
            await update.message.reply_text(
                "⛔ 5 جار تەواو بوو\nتا بەیانی ناتوانیت",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            save(data)
            return
        data["free"][uid]["count"] += 1
        save(data)

    msg = await update.message.reply_text("🤖 بیر دەکەمەوە...")

    try:
        r = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":text}]
        )
        await msg.edit_text(r.choices[0].message.content)
    except:
        await msg.edit_text("❌ هەڵە لە AI")
# ==============================================

# ================== ▶️ RUN ==================
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
# ==============================================