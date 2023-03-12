import telebot
from telebot import types
import sqlite3
from setting import *

bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, coins INTEGER DEFAULT 0)')


# Функция для добавления extremecoins пользователю
def add_coins(user_id, coins):
    cursor.execute('SELECT coins FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        current_coins = result[0]
        new_coins = current_coins + coins
        cursor.execute('UPDATE users SET coins = ? WHERE id = ?', (new_coins, user_id))
    else:
        cursor.execute('INSERT INTO users (id, coins) VALUES (?, ?)', (user_id, coins))
    conn.commit()


# Функция для получения текущего баланса extremecoins пользователя
def get_balance(user_id):
    cursor.execute('SELECT coins FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я бот, который раздаёт extremecoins за выполнение заданий. Напиши /help, чтобы узнать, как начать.")


#Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
# Создание таблицы пользователей, если её ещё нет
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
              (user_id INTEGER PRIMARY KEY, 
               first_name TEXT, 
               last_name TEXT,
               username TEXT,
               balance INTEGER DEFAULT 0,
               rating INTEGER DEFAULT 0)''')

# Добавление нового пользователя в базу данных, если его ещё нет
user_id = message.from_user.id
first_name = message.from_user.first_name
last_name = message.from_user.last_name
username = message.from_user.username

cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, username))
conn.commit()

# Отправка сообщения с приветствием и инструкцией
bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я бот, который раздаёт extremecoins за выполнение заданий. Напиши /help, чтобы узнать, как начать.")

# Закрытие соединения с базой данных
conn.close()
#Запуск бота
if name == 'main':
    bot.polling(none_stop=True)

#Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '''Я могу выполнить следующие команды:
    /start - начать работу со мной
    /help - получить информацию о командах бота
    /balance - показать текущий баланс extremecoins
    /tasks - показать доступные задания для заработка extremecoins
    /convert - обменять свои extremecoins на внутренние баллы рейтинга
    ''')

#Команда /tasks
@bot.message_handler(commands=['tasks'])
def tasks(message):
    user_id = message.from_user.id
    tasks = get_available_tasks()
    markup = types.InlineKeyboardMarkup()
    for task in tasks:
        button_text = f"{task['name']} ({task['reward']} extremecoins)"
        button_callback = f"task:{task['id']}"
        if is_task_completed(user_id, task['id']):
            button_text += " ✅"
            button_callback = ""
        markup.add(types.InlineKeyboardButton(text=button_text, callback_data=button_callback))
    bot.send_message(message.chat.id, "Доступные задания:", reply_markup=markup)

#Команда /convert
@bot.message_handler(commands=['convert'])
def convert(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    if balance == 0:
        bot.send_message(message.chat.id, "У тебя нет extremecoins для обмена")
        return
    rating_points = balance * EXCH_RATE
    update_balance(user_id, -balance)
    update_rating_points(user_id, rating_points)
    bot.send_message(message.chat.id, f"Ты обменял {balance} extremecoins на {rating_points} внутренних баллов рейтинга")

#Обработка inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    if call.data.startswith("task:"):
        task_id = int(call.data.split(":")[1])
        task = get_task(task_id)
        reward = task['reward']
        if not is_task_completed(user_id, task_id):
            update_balance(user_id, reward)
            add_completed_task(user_id, task_id)
            bot.answer_callback_query(call.id, f"Ты получил {reward} extremecoins за выполнение задания")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Задание выполнено! Вот другие доступные задания:")
            tasks(call.message)
        else:
            bot.answer_callback_query(call.id, "Ты уже выполнил это задание")
    elif call.data == "balance":
        balance(call.message)
    elif call.data == "tasks":
        tasks(call.message)
    elif call.data == "convert":
        convert(call.message)

@bot.message_handler(commands=['advert'])
def advert(message):
    user_id = message.from_user.id
    if user_id == admin_id:
        markup = types.InlineKeyboardMarkup()
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()
       
#Запуск бота
if name == 'main':
    bot.polling(none_stop=True)

#Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '''Я могу выполнить следующие команды:
    /start - начать работу со мной
    /help - получить информацию о командах бота
    /balance - показать текущий баланс extremecoins
    /tasks - показать доступные задания для заработка extremecoins
    /convert - обменять свои extremecoins на внутренние баллы рейтинга
    ''')

#Команда /tasks
@bot.message_handler(commands=['tasks'])
def tasks(message):
    user_id = message.from_user.id
    tasks = get_available_tasks()
    markup = types.InlineKeyboardMarkup()
    for task in tasks:
        button_text = f"{task['name']} ({task['reward']} extremecoins)"
        button_callback = f"task:{task['id']}"
        if is_task_completed(user_id, task['id']):
            button_text += " ✅"
            button_callback = ""
        markup.add(types.InlineKeyboardButton(text=button_text, callback_data=button_callback))
    bot.send_message(message.chat.id, "Доступные задания:", reply_markup=markup)

#Команда /convert
@bot.message_handler(commands=['convert'])
def convert(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    if balance == 0:
        bot.send_message(message.chat.id, "У тебя нет extremecoins для обмена")
        return
    rating_points = balance * EXCH_RATE
    update_balance(user_id, -balance)
    update_rating_points(user_id, rating_points)
    bot.send_message(message.chat.id, f"Ты обменял {balance} extremecoins на {rating_points} внутренних баллов рейтинга")

#Обработка inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    if call.data.startswith("task:"):
        task_id = int(call.data.split(":")[1])
        task = get_task(task_id)
        reward = task['reward']
        if not is_task_completed(user_id, task_id):
            update_balance(user_id, reward)
            add_completed_task(user_id, task_id)
            bot.answer_callback_query(call.id, f"Ты получил {reward} extremecoins за выполнение задания")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Задание выполнено! Вот другие доступные задания:")
            tasks(call.message)
        else:
            bot.answer_callback_query(call.id, "Ты уже выполнил это задание")
    elif call.data == "balance":
        balance(call.message)
    elif call.data == "tasks":
        tasks(call.message)
    elif call.data == "convert":
        convert(call.message)

@bot.message_handler(commands=['advert'])
def advert(message):
    user_id = message.from_user.id
    if user_id == admin_id:
        markup = types.InlineKeyboardMarkup()
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()
       
# Отправка рекламы
rows = cursor.execute("SELECT * FROM users WHERE is_admin = 0").fetchall()
if rows:
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        balance = row[2]
        user_markup = types.InlineKeyboardButton(row[1], callback_data=f"advert_{row[0]}")
        markup.add(user_markup)
    bot.send_message(message.chat.id, "Выберите пользователя, которому хотите отправить рекламу:", reply_markup=markup)
else:
    bot.send_message(message.chat.id, "Эта команда доступна только администратору бота.")
# Просмотр и изменение рекламы
if advert_id:
    query = "SELECT * FROM adverts WHERE advert_id = ?"
    cursor.execute(query, (advert_id,))
    advert_row = cursor.fetchone()
    if advert_row:
        advert_cost = advert_row[1]
        advert_desc = advert_row[2]
        if not action:
            # Просмотр информации о рекламе
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Удалить рекламу", callback_data=f"delete_advert:{advert_id}"))
            markup.add(types.InlineKeyboardButton("Изменить стоимость рекламы", callback_data=f"change_price:{advert_id}"))
            bot.send_message(admin_id, f"Реклама с ID {advert_id} найдена:\n"
                                       f"Стоимость: {advert_cost} extremecoins\n"
                                       f"Описание: {advert_desc}", reply_markup=markup)
        else:
            # Изменение стоимости рекламы
            if action.startswith("change_price:"):
                new_cost = int(action.split(':')[1])
                query = "UPDATE adverts SET advert_cost = ? WHERE advert_id = ?"
                cursor.execute(query, (new_cost, advert_id))
                conn.commit()
                bot.send_message(admin_id, f"Стоимость рекламы с ID {advert_id} изменена на {new_cost} extremecoins.")
            # Удаление рекламы
            elif action.startswith("delete_advert:"):
                query = "DELETE FROM adverts WHERE advert_id = ?"
                cursor.execute(query, (advert_id,))
                conn.commit()
                bot.send_message(admin_id, f"Реклама с ID {advert_id} удалена.")
            else:
                bot.send_message(admin_id, "Неизвестное действие.")
    else:
        bot.send_message(admin_id, "Реклама не найдена.")
else:
    bot.send_message(admin_id, "Укажите ID рекламы, которую хотите просмотреть.")


