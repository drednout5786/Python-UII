# LIGHT:
# создать простейшего чат-бота в Telegram, обработать ответы не менее, чем на 3 фразы и 3 команды.
# PRO:
# реализовать чат-бота с некоторой логикой. Например, можно реализовать чат-бота:
# 1. еженедельник (можно вносить планы, спрашивать бота что по плану на завтра и т.д.).

import telebot
from telebot import apihelper
import config
import json, datetime
from dateutil.parser import parse
# from config import TOKEN

# import time
# from multiprocessing.context import Process
import schedule

# import sqlite3 # база данных на движке SQLite
# import random
# import time
# import json
# random.seed()
# pip install emoji


TOKEN = config.token

proxies = {
    'http': 'http://51.158.180.179:8811',
    'https': 'http://51.158.180.179:8811',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

# Клавиатура
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # Делает узкие (True) кнопки и Прячем клавиатуру после одного нажатия - True
keyboard1.row('Привет', 'Пока', 'СГК', 'Помощь')


keyboard_sgk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
keyboard_sgk.row('Узнать планы', 'Запланировать', 'Сделать расчеты')

keyboard_ya = telebot.types.InlineKeyboardMarkup()

# Функция проверки авторизации
def autor(chatid):
    strid = str(chatid)
    for item in config.users:
        if item == strid:
            return True
    return False

# Функция создания json файла с данными
def add_info(js_path, user_id, date, act):
    try:
        with open(js_path, mode='r', encoding="utf8") as json_file:
            json_data = json.load(json_file)
        print(json_data)
        if len(json_data) < 1:
            print('empty file')
        if user_id not in json_data.keys():
            json_data.update({user_id: []})
        json_data[user_id].append(dict(date=date, action=act))
        # Сейчас сохранение происходит каждый раз. Хочу сделать, чтобы сохранение на внешний носитель было раз в сутки.
        with open(js_path, mode='w', encoding="utf8") as json_file:
             json.dump(json_data, json_file, ensure_ascii=False)
        # json_data.clear() # очищаем словарь
        return json_data
    except Exception as e:
        print(e)

# комманда start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Привет, ' + user_name + '! Я робот Ленин. Нажми /help, чтобы получить список команд. Или выбери из меню ниже.', reply_markup=keyboard1)

# комманда help
@bot.message_handler(commands=['help'])
def all_commands(message):
    bot.send_message(message.chat.id, '/start - начало работы\n/admin - для админа\n/help - помощь (список комманд)\n/sgk - расчеты по СГК\n/search - Поиск в Яндекс\n/geophone - запрос телефона и геоданных\n/rm - убрать кнопки с меню\n/stop - окончание работы')

# комманда admin
@bot.message_handler(commands=['admin'])
def admin(message):
    user_name = message.from_user.first_name
    if autor(message.chat.id):
        bot.send_message(message.chat.id, 'Приветствую тебя, ' + user_name + '! Мой Создатель!')
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    else:
        bot.send_message(message.chat.id, 'Привет, ' + user_name + '! Ты не мой Хозяин! Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

# комманда СГК (sgk)
@bot.message_handler(commands=['sgk'])
def description(message):
    bot.send_message(message.chat.id, 'Расчеты по СГК. Выберите из меню ниже.', reply_markup=keyboard_sgk)

# комманда поиск (search)
@bot.message_handler(commands=['search'])
def description(message):
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard_ya.add(url_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы перейди в поисковик.", reply_markup=keyboard_ya)

# комманда stop
@bot.message_handler(commands=['stop'])
def send_something(message):
    bot.send_message(message.chat.id, 'Да свидания! Приятно было пообщаться!')
    bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')

# комманда geophone
@bot.message_handler(commands=["geophone"])
def geophone(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона ☎️", request_contact=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение 🗺️", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id, "Отправь мне свой номер телефона или поделись местоположением! Так нам легче будет с Вами связаться.", reply_markup=keyboard)

# комманда убрать кнопки с меню
@bot.message_handler(commands=["rm"])
def process_rm_command(message):
    bot.send_message(message.chat.id, "Убираем шаблоны сообщений. Если нужна помощь, то нажми /help - помощь (список комманд).", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    # print(message.from_user.first_name)
    print(message.sticker.emoji)
    print(message.sticker.file_id)
    if message.sticker.set_name == 'PresidentPutin':
        print(message.from_user.first_name)

# Сохраняем присланый от пользователя файл в текущую папку - подпапку received/ с указанием chat.id
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'received/' + str(message.chat.id) + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Ваш файл '" + message.document.file_name + "' получен и сохранен у меня.")
    except Exception as e:
        bot.reply_to(message, e)

# “ловит” он только те сообщения, которые отредактированы
@bot.edited_message_handler(func=lambda message: True)
def edit_message(message):
    bot.edit_message_text(chat_id=message.chat.id,
                          text= "Вы отредактировали свое сообщение на: '{!s}'".format(message.text),
                          message_id=message.message_id + 1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    # print(message)
    user_name = message.from_user.first_name
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, '+ user_name + '!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, '+ user_name + '! Приятно было пообщаться!')
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    elif message.text.lower() == 'узнать планы':
        bot.send_message(message.chat.id, 'Сейчас все расскажу.')
    elif message.text.lower() == 'запланировать':
        user_name = message.from_user.first_name
        if autor(message.chat.id):
            # Пока это очень рабочий вариант. Без запроса от пользователя даты и что делать надо будет.
            print("1:", add_info('personal.json', '127', '2022.09.10', 'анализ'))
            bot.send_message(message.chat.id, 'Давай планировать!')
        else:
            bot.send_message(message.chat.id,
                             'У Вас, ' + user_name + ', нет доступа к планированию. Доступ возможен только Админу.')
    elif message.text.lower() == 'сделать расчеты':
        bot.send_message(message.chat.id, 'Давай считать! Но позже, пока меня этому не обучили. Доступ к расчетам будет только у Админа.')
    elif message.text.lower() == 'помощь':
        bot.send_message(message.chat.id, '/start - начало работы\n/admin - для админа\n/help - помощь (список комманд)\n/sgk - расчеты по СГК\n/search - Поиск в Яндекс\n/geophone - запрос телефона и геоданных\n/rm - убрать кнопки с меню\n/stop - окончание работы')
    # elif message.text.lower() == 'я тебя люблю':
    #     bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    else:
        # message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
        #                     italic('\nЯ просто напомню,'), 'что есть',
        #                     code('команда'), '/help')
        # bot.send_message(message.chat.id, message_text)
        if message.text == 'sticker':
            bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
        else:
            bot.send_message(message.chat.id, 'Я не понял команду. Если нужна помощь, то нажми /help - помощь (список комманд)')

# обработка неизвестных нетекстовых сообщений
# @bot.message_handler(content_types=ContentType.ANY)
# def unknown_message(message):
#     message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
#                         italic('\nЯ просто напомню,'), 'что есть',
#                         code('команда'), '/help')
#     bot.send_message(message.chat.id, message_text, parse_mode=ParseMode.MARKDOWN)

try:
    bot.polling(none_stop=True, interval=0)
    while true:
        print ('while true') #Этот принт не работает...
        # Думала сюда поставить запуск функции раз в сутки сохранять json на внешний носитель.
except:
    pass


# PS
# bot.polling(none_stop=True, interval=0) # Это нужно для того, чтобы бот не выключился сразу, а работал и проверял, нет ли на сервере нового сообщения.
# bot.infinity_polling() # запускает т.н. Long Polling
# https://habr.com/ru/post/448310/
# Учебник Пишем ботов для Telegram на языке Python https://mastergroosha.github.io/telegram-tutorial/
# https://flammlin.com/blog/2020/01/19/python-telegram-bot/
# https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html