import telebot
from telebot import types
import os

bot = telebot.TeleBot('bot_token')

balance_file = 'balance.txt'
promo_codes = {
    'DIANA': ' Баланс обнулён !',
    'STAN': ' Баланс обнулён !'
}

# --- ФУНКЦИИ РАБОТЫ С БАЛАНСОМ ---
def load_balance():
    if os.path.exists(balance_file):
        with open(balance_file, 'r') as f:
            return int(f.read().strip())
    return 0

def save_balance(balance):  # <-- ИСПРАВЛЕНО: добавлен аргумент
    with open(balance_file, 'w') as f:
        f.write(str(balance))  # <-- ИСПРАВЛЕНО: записываем переданный баланс

# Загружаем баланс при старте
friend_balance = load_balance()

# --- КЛАВИАТУРА ---
def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('➕ 1 респект', '➕ 3 респекта', '➕ 5 респектов')
    markup.add('📊 Баланс', '🎁 Ввести промокод')
    return markup

# --- КОМАНДЫ ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f"Привет! Добро пожаловать в Beresta Wallet!\n"
                     f"Здесь вы можете начислять респекты Бересте почти за всё!\n"
                     f"Текущий баланс Бересты: {friend_balance}\n"
                     f"© Beresta Wallet is made by BRATVA",
                     reply_markup=create_keyboard())

# --- ОБРАБОТКА КНОПОК ---
@bot.message_handler(func=lambda message: message.text in [
    '➕ 1 респект', '➕ 3 респекта', '➕ 5 респектов', '📊 Баланс'
])
def handle_buttons(message):
    global friend_balance
    if message.text == '➕ 1 респект':
        friend_balance += 1
        text = "Спасибо друг!"
        bot.send_message(message.chat.id, text)
    elif message.text == '➕ 3 респекта':
        friend_balance += 3
        text = "Суперспасибо дружище!"
        bot.send_message(message.chat.id, text)
    elif message.text == '➕ 5 респектов':
        friend_balance += 5
        text = "ТУРБО СПАСИБО КЕНТАФУРИК!"
        bot.send_message(message.chat.id, text)
    elif message.text == '📊 Баланс':
        text = f"Текущий баланс респектов: {friend_balance}"
        bot.send_message(message.chat.id, text)
        return  # Не сохраняем баланс, т.к. он не менялся

    # СОХРАНЯЕМ БАЛАНС ПОСЛЕ ИЗМЕНЕНИЯ!
    save_balance(friend_balance)


# --- ПРОМОКОДЫ ---
@bot.message_handler(func=lambda message: message.text == '🎁 Ввести промокод')
def ask_promo(message):
    msg = bot.send_message(message.chat.id, "Введите промокод:")
    bot.register_next_step_handler(msg, process_promo)

def process_promo(message):
    global friend_balance
    promo = message.text.strip().upper()

    if promo in promo_codes:
        friend_balance = 0
        save_balance(friend_balance)
        bot.send_message(message.chat.id, promo_codes[promo])
        return
    else:
        bot.send_message(message.chat.id, "❌ Неверный промокод.")

# --- ЗАПУСК ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()