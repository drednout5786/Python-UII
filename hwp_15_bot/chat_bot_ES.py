# LIGHT:
# создать простейшего чат-бота в Telegram, обработать ответы не менее, чем на 3 фразы и 3 команды.
# PRO:
# реализовать чат-бота с некоторой логикой. Например, можно реализовать чат-бота:
# 1. еженедельник (можно вносить планы, спрашивать бота что по плану на завтра и т.д.).

import telebot
from telebot import apihelper
import config
import re
import json, datetime
from dateutil.parser import parse

TOKEN = config.token
ADMIN_MAIN_ID = config.users[0]

proxies = config.proxies

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

# Клавиатуры
# Делает узкие resize_keyboard=True кнопки и Прячем клавиатуру после одного нажатия (one_time_keyboard) - True
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
keyboard1.row('Привет', 'Пока', 'СГК', 'Помощь')


keyboard_sgk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
keyboard_sgk.row('Узнать планы', 'Запланировать', 'Сделать расчеты')

keyboard_ya = telebot.types.InlineKeyboardMarkup()

# Паттерны
pattern_date = r'\d{4}.\d{2}.\d{2}'
# [a-zA-Z0-9]+
# r'w+', # последовательность букв или цифр

# Путь для сохранения данных, полученных от Пользователя
path = 'personal.json'

##################################################################################################
# Функция проверки авторизации
def autor(chatid):
    strid = str(chatid)
    for item in config.users:
        if item == strid:
            return True
    return False

# комманда СГК (sgk) - действие
def sgk_command_action(message):
    sgk_date = re.search(pattern_date, message.text)  # ищем дату по шаблону
    if sgk_date is not None:
        s = sgk_date.start()
        e = sgk_date.end()
        user_id = str(message.chat.id)
        try:
            with open(path, 'r', encoding="utf8") as json_file:
                json_data = json.load(json_file)
            # user_id = str(user_id)
            if user_id not in json_data.keys():
                json_data.update({user_id: []})
            json_data[user_id].append(dict(user_name=message.from_user.first_name,date=message.text[s:e],
                                           action=message.text[e:].strip()))
            with open(path, 'w', encoding="utf8") as json_file:
                json.dump(json_data, json_file, ensure_ascii=False)
                bot.send_message(message.chat.id, 'Бот сохранил твое задание. На дату: ' + message.text[s:e] +
                                 '\nнамечено выполнение: ' + message.text[e:].strip(), reply_markup=keyboard_sgk)
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.chat.id, message.from_user.first_name +
                         ', Бот не может правильно распознать введенную тобой дату. Повтори ввод еще раз. ' +
                         'Для этого нажми еще раз кнопку Запланировать и еще раз введи задание.\n' +
                         ' Формат ввода: ' + ' ГГГГ.ММ.ДД Текст действия.' +
                         'Или нажми /help - помощь (список комманд).')

# комманда start
@bot.message_handler(commands=['start'])
def process_start_command(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Привет, ' + user_name +
                     '! Я робот Умка. Нажми /help, чтобы получить список команд. Или выбери из меню ниже.',
                     reply_markup=keyboard1)

# комманда help
@bot.message_handler(commands=['help'])
def process_help_command(message):
    bot.send_message(message.chat.id,
                     '/start - начало работы\n' +
                     '/admin - для админа\n' +
                     '/help - помощь (список комманд)\n' +
                     '/url - переход на наш сайт\n' +
                     '/search - Поиск в Яндекс\n' +
                     '/geophone - запрос телефона и геоданных\n' + # Данные Пользователя пока нигде не сохраняются
                     '/rm - убрать кнопки с меню', reply_markup=keyboard1)

# комманда admin
@bot.message_handler(commands=['admin'])
def admin(message):
    user_name = message.from_user.first_name
    if autor(message.chat.id):
        bot.send_message(message.chat.id, 'Приветствую тебя, ' + user_name + '! Мой Создатель!')
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    else:
        bot.send_message(message.chat.id, 'Привет, ' + user_name + '! Ты не мой Хозяин! Твой ID: ' +
                         str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

# комманда поиск (search)
@bot.message_handler(commands=['search'])
def process_search_command(message):
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard_ya.add(url_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы перейди в поисковик.", reply_markup=keyboard_ya)

# комманда geophone # Данные Пользователя пока нигде не сохраняются
@bot.message_handler(commands=["geophone"])
def geophone(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона ☎️", request_contact=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение 🗺️", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id, "Отправь мне свой номер телефона или поделись местоположением!" +
                     " Так нам легче будет с Вами связаться.", reply_markup=keyboard)

# комманда убрать кнопки с меню
@bot.message_handler(commands=["rm"])
def process_rm_command(message):
    bot.send_message(message.chat.id, "Убрал шаблоны сообщений. Если нужна помощь, то нажми\n" +
                                      "/help - помощь (список комманд).",
                     reply_markup=telebot.types.ReplyKeyboardRemove())

# комманда Перейти на сайт - url
@bot.message_handler(commands = ['url'])
def process_url_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_my_site = telebot.types.InlineKeyboardButton(text='Наш сайт', url='https://www.ranepa.ru')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)

# Действие Бота, если Пользователь прислал Стикер
@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    if message.sticker.emoji == '🤔': # Стикер с вопросом
        bot.send_message(message.chat.id, 'Нажми /help, чтобы получить список команд.')
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDG16BpcFCgjXYVVATRCBaxrOd60oFAAIBJQACns4LAAG3W39juSKGHxgE')
    # if message.sticker.set_name == 'PresidentPutin':
    #     bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

# Сохраняем присланый от Пользователя файл в текущую папку - подпапку received/ с указанием chat.id
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'received/' + str(message.chat.id) + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Твой файл '" + message.document.file_name + "' получен и сохранен у меня.")
    except Exception as e:
        bot.reply_to(message, e)

# “ловит” он только те сообщения, которые отредактированы Пользователем
@bot.edited_message_handler(func=lambda message: True)
def edit_message(message):
    bot.edit_message_text(chat_id=message.chat.id,
                          text= "Ты отредактировал свое сообщение на: '{!s}'".format(message.text),
                          message_id=message.message_id + 1)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):
    user_name = message.from_user.first_name

    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, '+ user_name + '!')

    elif message.text.lower() == 'пока':
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='Да')
        keyboard.add(key_yes)
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='Нет')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, 'Ты действительно хочешь покинуть чат со мной??', reply_markup=keyboard)

    elif message.text.lower() == 'сгк':
        bot.send_message(message.chat.id, 'Работа с СГК. Выбери из меню ниже.', reply_markup=keyboard_sgk)

    elif message.text.lower() == 'узнать планы':
        date = datetime.datetime.today()
        # print('date = ', date)
        with open(path, mode='r', encoding="utf8") as json_file:
            json_data = json.load(json_file)
        str_all = ''
        for key in json_data.keys():
            for i in range(len(json_data[key])):
                if parse(json_data[key][i]['date']) > date:
                    iter_key = json_data[key][i]
                    str_all = str_all + key + ' ' + iter_key['user_name'] + ' ' + iter_key['date'] + ' ' + \
                              iter_key['action'] + '\n'
        bot.send_message(message.chat.id, 'Запланированы следующие действия:\n' + str_all, reply_markup=keyboard_sgk)
        # bot.send_message(message.chat.id, 'Сейчас все расскажу.', reply_markup=keyboard_sgk)

    elif message.text.lower() == 'запланировать':
        user_name = message.from_user.first_name
        if autor(message.chat.id):
            sent = bot.send_message(message.chat.id,
                                    'Укажите когда и что Вы хотите запланировать в формате ГГГГ.ММ.ДД Текст действия.',
                                    reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(sent, sgk_command_action)
        else:
            bot.send_message(message.chat.id,
                             'У тебя, ' + user_name + ', нет доступа к планированию. Доступ возможен только Админу.')

    elif message.text.lower() == 'сделать расчеты':
        bot.send_message(message.chat.id, 'Давай считать! Но позже, пока меня этому не обучили.\n' +
                         'Пока тут стоит заглушка.', reply_markup=keyboard_sgk)

    elif message.text.lower() == 'помощь':
        bot.send_message(message.chat.id,
                         '/start - начало работы\n' +
                         '/admin - для админа\n' +
                         '/help - помощь (список комманд)\n' +
                         '/url - переход на наш сайт\n' +
                         '/search - Поиск в Яндекс\n' +
                         '/geophone - запрос телефона и геоданных\n' +
                         '/rm - убрать кнопки с меню')
    # elif message.text.lower() == 'я тебя люблю':
    #     bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

    # Реакция по Дефолту
    else:
        bot.send_message(message.chat.id,
                         'Я не понял команду. Если нужна помощь, то нажми /help - помощь (список комманд)')
        # message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
        #                     italic('\nЯ просто напомню,'), 'что есть',
        #                     code('команда'), '/help')

# Подтверждение выхода из Бота
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):
    user_name = call.message.chat.first_name
    if call.data == 'Да':
        bot.answer_callback_query(call.id) # убрает состояние загрузки, к которому переходит бот после нажатия кнопки
        bot.send_message(call.message.chat.id, 'Прощай, ' + user_name + '! Приятно было пообщаться!')
        bot.send_sticker(call.message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Ура! ' + user_name + ', давай продолжим! :)')

###########################################################################################################
# Активация Бота
try:
    bot.polling(none_stop=True, interval=0)
    # Это нужно для того, чтобы бот не выключился сразу, а работал и проверял, нет ли на сервере нового сообщения.
except:
    pass
###########################################################################################################

# PS
# bot.infinity_polling() # запускает т.н. Long Polling
# https://habr.com/ru/post/448310/
# Учебник Пишем ботов для Telegram на языке Python https://mastergroosha.github.io/telegram-tutorial/
# https://flammlin.com/blog/2020/01/19/python-telegram-bot/
# https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html
# https://www.cyberforum.ru/python-web/thread2514386.html
# print("1:", add_info('personal.json', '127', '2022.09.10', 'анализ'))
# https://pythonru.com/primery/python-telegram-bot#-6-exchange

# Календарь https://habr.com/ru/post/335886/