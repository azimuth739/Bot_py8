import telebot
from telebot import types

TOKEN = "8815891915:AAESN91FeDze_uU_2CbrYCyN30nza0jh_eM"
bot = telebot.TeleBot ( TOKEN)

# Хранилище заявок (в памяти)
user_data = {}

@bot.message_handler ( commands=['start'])
def start ( message ) :
    markup = types.ReplyKeyboardMarkup ( resize_keyboard=True)
    btn1 = types.KeyboardButton ( "✈️ Пилот")
    btn2 = types.KeyboardButton ( "🛫 Бортпроводник")
    btn3 = types.KeyboardButton ( "👔 Администратор")
    markup.add ( btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в AzimuthAirlines_RBLX!\n"
        "Выбери должность, на которую хочешь подать заявку:",
        reply_markup=markup
    )

@bot.message_handler ( func=lambda msg: msg.text in ["✈️ Пилот", "🛫 Бортпроводник", "👔 Администратор"])
def choose_position ( message ) :
    position = message.text.replace ( "✈️ ", "" ) .replace ( "🛫 ", "" ) .replace ( "👔 ", "")
    user_data[message.chat.id] = {"position": position}
    
    bot.send_message(
        message.chat.id,
        f"Отлично! Заявка на {position}.\n"
        "Теперь напиши своё Имя и Фамилию (в Roblox ) :"
    )
    bot.register_next_step_handler ( message, get_fullname)

def get_fullname ( message ) :
    user_data[message.chat.id]["fullname"] = message.text
    bot.send_message(
        message.chat.id,
        "Сколько тебе лет? (напиши цифру ) "
    )
    bot.register_next_step_handler ( message, get_age)

def get_age ( message ) :
    if not message.text.isdigit (  ) :
        bot.send_message ( message.chat.id, "Напиши возраст цифрой!")
        bot.register_next_step_handler ( message, get_age)
        return
    user_data[message.chat.id]["age"] = message.text
    bot.send_message(
        message.chat.id,
        "Напиши свой Discord (или @username в Telegram ) :"
    )
    bot.register_next_step_handler ( message, get_contact)

def get_contact ( message ) :
    user_data[message.chat.id]["contact"] = message.text
    bot.send_message(
        message.chat.id,
        "Есть ли у тебя опыт в авиации/администрировании? (кратко ) "
    )
    bot.register_next_step_handler ( message, get_experience)

def get_experience ( message ) :
    user_data[message.chat.id]["experience"] = message.text
    bot.send_message(
        message.chat.id,
        "Почему ты хочешь работать в AzimuthAirlines_RBLX?"
    )
    bot.register_next_step_handler ( message, get_reason)

def get_reason ( message ) :
    user_data[message.chat.id]["reason"] = message.text
    send_application ( message.chat.id)

def send_application ( chat_id ) :
    data = user_data[chat_id]
    
    # Формируем заявку
    text = (
        "📋 НОВАЯ ЗАЯВКА В AZIMUTHAIRLINES_RBLX\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Должность: {data['position']}\n"
        f"📛 Имя: {data['fullname']}\n"
        f"📅 Возраст: {data['age']}\n"
        f"📱 Контакты: {data['contact']}\n"
        f"📌 Опыт: {data['experience']}\n"
        f"💬 Мотивация: {data['reason']}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Заявка отправлена! Ожидай решения."
    )
    
    # Отправляем заявку тебе (владельцу) — укажи свой ID
    # Чтобы узнать свой ID, напиши боту /start и посмотри логи
    OWNER_ID = 8272176631  # ЗАМЕНИ НА СВОЙ TELEGRAM ID
    
    try:
        bot.send_message ( OWNER_ID, text)
        bot.send_message ( chat_id, "✅ Ваша заявка принята! Мы свяжемся с вами в ближайшее время.")
    except:
        bot.send_message ( chat_id, "❌ Ошибка отправки. Попробуй позже.")
    
    # Очищаем данные пользователя
    del user_data[chat_id]

# Запуск
bot.infinity_polling (  )