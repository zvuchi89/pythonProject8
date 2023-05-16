import telebot
import sqlite3

# Replace with your token
bot_token = "6073788864:AAE5WyhXvBCfA1ldDy_gRaOgQh7HYs86vHU"
bot = telebot.TeleBot(bot_token)

# Replace with your channel name
channel_name = "@loyalty_card_updates"

# Connect to the database
conn = sqlite3.connect("loyalty_card.db")
c = conn.cursor()

# Create the users' table
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, bought INTEGER, free INTEGER)''')
conn.commit()

# Create the channel
try:
    bot.get_chat(channel_name)
except telebot.apihelper.ApiException:
    bot.create_chat(channel_name, "Новости карты лояльности")

# Handle the "/start" command
@bot.message_handler(commands=['start'])
def welcome_message(message):
    user_id = message.chat.id
    user_name = message.chat.first_name
    bot.send_message(user_id, "Привет, {}! Я твой персональный бот для карты лояльности. Ты можешь отмечать у меня купленные напитки, чтобы получить бесплатный напиток. Для того, чтобы начать, отправь мне /register".format(user_name))

# Handle the "/register" command
@bot.message_handler(commands=['register'])
def register_message(message):
    user_id = message.chat.id
    user_name = message.chat.first_name
    c.execute('''INSERT INTO users (id, name, bought, free) VALUES (?, ?, ?, ?)''', (user_id, user_name, 0, 0))
    conn.commit()
    bot.send_message(user_id, "Ты успешно зарегистрировался на карту лояльности")
