from telegram import (
    Bot,
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonCommands,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8941079776:AAHwD3FyDTlHJINnO1FmAdB79EaS--_W3uM"

# ─── 10 сұрақ ────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "question": '"Жақсырақ" қай шырай?',
        "options": ["A) Жай", "B) Салыстырмалы", "C) Күшейтпелі"],
        "answer": 1,
    },
    {
        "question": '"Өте үлкен" қай шырай?',
        "options": ["A) Жай", "B) Салыстырмалы", "C) Күшейтпелі"],
        "answer": 2,
    },
    {
        "question": '"Әдемі" сөзі қай шырайға жатады?',
        "options": ["A) Жай", "B) Салыстырмалы", "C) Күшейтпелі"],
        "answer": 0,
    },
    {
        "question": '"Биікірек" қай шырай?',
        "options": ["A) Күшейтпелі", "B) Жай", "C) Салыстырмалы"],
        "answer": 2,
    },
    {
        "question": '"Аппақ" қай шырай?',
        "options": ["A) Жай", "B) Күшейтпелі", "C) Салыстырмалы"],
        "answer": 1,
    },
    {
        "question": "Салыстырмалы шырай қандай жұрнақтар арқылы жасалады?",
        "options": ["A) -лау, -леу", "B) -рақ, -рек, -ырақ, -ірек", "C) өте, тым, ең"],
        "answer": 1,
    },
    {
        "question": "Күшейтпелі шырай қандай сөздермен жасалады?",
        "options": ["A) -рақ, -рек", "B) -лы, -лі", "C) өте, тым, ең, аса"],
        "answer": 2,
    },
    {
        "question": '"Ең жылдам" деген тіркес қай шырай?',
        "options": ["A) Жай", "B) Салыстырмалы", "C) Күшейтпелі"],
        "answer": 2,
    },
    {
        "question": '"Кішірек" сөзі қай шырайға жатады?',
        "options": ["A) Салыстырмалы", "B) Жай", "C) Күшейтпелі"],
        "answer": 0,
    },
    {
        "question": "Жай шырай дегеніміз не?",
        "options": [
            "A) Сапаның өте жоғары дәрежесі",
            "B) Сын есімнің негізгі, өзгеріссіз түрі",
            "C) Екі затты салыстыру",
        ],
        "answer": 1,
    },
]

# ─── Негізгі мәзір батырмалары ───────────────────────────────────────────────
MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("📖 Теория",   callback_data="theory")],
    [InlineKeyboardButton("📊 Кесте",    callback_data="table")],
    [InlineKeyboardButton("✏️ Жаттығу", callback_data="practice")],
    [InlineKeyboardButton("🧪 Тест",     callback_data="test")],
])


def get_question_keyboard(q_index: int) -> InlineKeyboardMarkup:
    q = QUESTIONS[q_index]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(opt, callback_data=f"ans_{q_index}_{i}")]
        for i, opt in enumerate(q["options"])
    ])


# ─── /start ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Сын есімнің шырайлары бойынша оқу ботына қош келдіңіз!\n\n"
        "Төмендегі мәзірден бөлімді таңдаңыз:",
        reply_markup=MAIN_MENU,
    )


# ─── /theory, /table, /practice, /test — команда арқылы ашу ─────────────────
async def cmd_theory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_theory(update.message)

async def cmd_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_table(update.message)

async def cmd_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_practice(update.message)

async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["score"] = 0
    context.user_data["q_index"] = 0
    q = QUESTIONS[0]
    await update.message.reply_text(
        "🧪 Тест басталды! 10 сұрақ.\n\n"
        f"Сұрақ 1/10:\n{q['question']}",
        reply_markup=get_question_keyboard(0),
    )


# ─── Мазмұн функциялары ───────────────────────────────────────────────────────
async def send_theory(msg):
    await msg.reply_text(
        "📖 Шырай түрлері\n\n"
        "1️⃣ Жай шырай\n"
        "Сын есімнің негізгі, өзгеріссіз түрі.\n"
        "Мысалы: жақсы, әдемі, үлкен, биік.\n\n"
        "2️⃣ Салыстырмалы шырай\n"
        "Бір заттың сапасын екінші затпен салыстырады.\n"
        "Жұрнақтар: -рақ / -рек / -ырақ / -ірек\n"
        "Мысалы: жақсырақ, үлкенірек, биігірек.\n\n"
        "3️⃣ Күшейтпелі шырай\n"
        "Сапаның өте жоғары дәрежесін білдіреді.\n"
        "Жасалу жолдары:\n"
        "  • өте, тым, ең, аса + сын есім → өте жақсы, ең үлкен\n"
        "  • Буын қайталау → аппақ, сарғыш\n"
        "Мысалы: өте жақсы, тым үлкен, аппақ, ең биік."
    )


async def send_table(msg):
    await msg.reply_text(
        "📊 Шырайлар кестесі\n\n"
        "┌─────────────────┬──────────────┬──────────────────────┐\n"
        "│   Шырай түрі   │    Мысал     │     Ерекшелігі       │\n"
        "├─────────────────┼──────────────┼──────────────────────┤\n"
        "│ Жай шырай       │ үлкен, жақсы │ Негізгі түрі         │\n"
        "│ Салыстырмалы    │ үлкенірек    │ Салыстыру (-рақ/-рек)│\n"
        "│ Күшейтпелі      │ өте үлкен    │ Күшейту (өте, ең)    │\n"
        "└─────────────────┴──────────────┴──────────────────────┘\n\n"
        "Жасалу жұрнақтары:\n"
        "• Салыстырмалы: -рақ, -рек, -ырақ, -ірек\n"
        "• Күшейтпелі: өте / тым / ең / аса + сын есім\n"
        "  немесе буын қайталау: аппақ, сарғыш"
    )


async def send_practice(msg):
    await msg.reply_text(
        "✏️ Жаттығу тапсырмалары\n\n"
        "1. «Жақсы» сөзінен салыстырмалы шырай жасаңыз.\n"
        "   → жақсырақ ✅\n\n"
        "2. «Үлкен» сөзінен күшейтпелі шырай жасаңыз.\n"
        "   → өте үлкен / ең үлкен ✅\n\n"
        "3. «Әдемі» сөзі қай шырайға жатады?\n"
        "   → Жай шырай ✅\n\n"
        "4. «Биігірек» сөзін талдаңыз.\n"
        "   → биік + ірек = салыстырмалы шырай ✅\n\n"
        "5. «Аппақ» сөзі қай шырай?\n"
        "   → Күшейтпелі шырай (буын қайталау) ✅"
    )


# ─── Батырма өңдегіші ─────────────────────────────────────────────────────────
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "theory":
        await send_theory(query.message)

    elif data == "table":
        await send_table(query.message)

    elif data == "practice":
        await send_practice(query.message)

    elif data == "test":
        context.user_data["score"] = 0
        context.user_data["q_index"] = 0
        q = QUESTIONS[0]
        await query.message.reply_text(
            "🧪 Тест басталды! 10 сұрақ.\n\n"
            f"Сұрақ 1/10:\n{q['question']}",
            reply_markup=get_question_keyboard(0),
        )

    elif data == "menu":
        await query.message.reply_text(
            "🏠 Басты мәзір:",
            reply_markup=MAIN_MENU,
        )

    elif data.startswith("ans_"):
        _, q_str, c_str = data.split("_")
        q_index = int(q_str)
        chosen  = int(c_str)

        if context.user_data.get("q_index", 0) != q_index:
            return  # қайталап баспасын

        correct = QUESTIONS[q_index]["answer"]
        score   = context.user_data.get("score", 0)

        if chosen == correct:
            score += 1
            feedback = "✅ Дұрыс!"
        else:
            feedback = f"❌ Қате. Дұрыс жауап: {QUESTIONS[q_index]['options'][correct]}"

        context.user_data["score"] = score
        next_index = q_index + 1
        context.user_data["q_index"] = next_index

        await query.message.reply_text(feedback)

        if next_index < len(QUESTIONS):
            q = QUESTIONS[next_index]
            await query.message.reply_text(
                f"Сұрақ {next_index + 1}/10:\n{q['question']}",
                reply_markup=get_question_keyboard(next_index),
            )
        else:
            percent = int(score / len(QUESTIONS) * 100)
            if percent == 100:
                grade = "🏆 Тамаша!"
            elif percent >= 80:
                grade = "⭐ Жақсы!"
            elif percent >= 60:
                grade = "👍 Орташа"
            else:
                grade = "📚 Қайталап оқы"

            await query.message.reply_text(
                f"🎉 Тест аяқталды!\n\n"
                f"Нәтиже: {score}/{len(QUESTIONS)} ({percent}%)\n"
                f"{grade}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Қайта тапсыру", callback_data="test")],
                    [InlineKeyboardButton("🏠 Басты мәзір",   callback_data="menu")],
                ]),
            )


# ─── Бот іске қосу ────────────────────────────────────────────────────────────
async def post_init(app):
    """Бот іске қосылғанда меню батырмасы мен командаларды орнату."""
    bot: Bot = app.bot
    await bot.set_my_commands([
        BotCommand("start",    "🏠 Басты мәзір"),
        BotCommand("theory",   "📖 Теория"),
        BotCommand("table",    "📊 Кесте"),
        BotCommand("practice", "✏️ Жаттығу"),
        BotCommand("test",     "🧪 Тест бастау"),
    ])
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    print("✅ Меню батырмасы орнатылды!")


app = (
    ApplicationBuilder()
    .token(TOKEN)
    .post_init(post_init)   # ← меню осында орнатылады
    .build()
)

app.add_handler(CommandHandler("start",    start))
app.add_handler(CommandHandler("theory",   cmd_theory))
app.add_handler(CommandHandler("table",    cmd_table))
app.add_handler(CommandHandler("practice", cmd_practice))
app.add_handler(CommandHandler("test",     cmd_test))
app.add_handler(CallbackQueryHandler(button))

print("🤖 Бот іске қосылды...")
app.run_polling()