import telebot
from telebot import types


BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

user_points = {}

# Пример расписания уроков
SCHEDULE = """
    🗓️ **Расписание уроков на неделю:**

    🟡 **Понедельник:**
    • 10:00–11:30 — Математика
    • 12:00–13:30 — Английский язык

    🔵 **Вторник:**
    • 09:00–10:30 — Физика
    • 11:00–12:30 — Программирование

    🟢 **Среда:**
    • 10:00–11:30 — История
    • 13:00–14:30 — Литература

    🟠 **Четверг:**
    • 09:00–10:30 — Химия
    • 11:00–12:30 — Биология

    🟣 **Пятница:**
    • 10:00–11:30 — География
    • 12:00–13:30 — Искусство
    """

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_points:
        user_points[user_id] = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📅 Получить расписание")
        btn2 = types.KeyboardButton("🏆 Мои баллы")
        markup.add(btn1, btn2)
        bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — бот твоей онлайн‑школы! Помогу с расписанием и начислю баллы за активность.\n\n"
        "Нажми на кнопку ниже, чтобы увидеть расписание уроков! ✨",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "📅 Получить расписание")
def send_schedule(message):
    user_id = message.from_user.id

bot.polling(none_stop=True, interval=0)