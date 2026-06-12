import telebot
from telebot import types


BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)


user_points = {}


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

    if user_id in user_points:
        user_points[user_id] += 100
    else:
        user_points[user_id] = 100

    level = get_user_level(user_points[user_id])

    bot.send_message(message.chat.id, SCHEDULE, parse_mode='Markdown')
    bot.send_message(
        message.chat.id,
        f"✅ Расписание отправлено!\n"
        f"🎯 Ты получил 100 баллов!\n"
        f"🏆 Твой текущий уровень: **{level}**\n"
        f"💰 Всего баллов: **{user_points[user_id]}**",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == "🏆 Мои баллы")
def show_points(message):
    user_id = message.from_user.id
    points = user_points.get(user_id, 0)
    level = get_user_level(points)

    bot.send_message(
        message.chat.id,
        f"👤 Твой профиль:\n\n"
        f"🏆 Уровень: **{level}**\n"
        f"💰 Баллы: **{points}**\n\n"
        f"Продолжай запрашивать расписание, чтобы повышать уровень! 🚀",
        parse_mode='Markdown'
    )

def get_user_level(points):
    """Определяет уровень пользователя по количеству баллов"""
    if points >= 1000:
        return "Эксперт"
    elif points >= 500:
        return "Профи"
    else:
        return "Новичок"


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(
        message.chat.id,
        "Не понял команду. Используй кнопки меню 👇",
        reply_markup=get_main_keyboard()
    )

def get_main_keyboard():
    """Создаёт клавиатуру с основными кнопками"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📅 Получить расписание")
    btn2 = types.KeyboardButton("🏆 Мои баллы")
    markup.add(btn1, btn2)
    return markup


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()