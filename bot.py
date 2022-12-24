import telebot
from telebot import types
import json
import random
import os
from dotenv import load_dotenv


class Catbot:

    NUMBER_OF_PICS: int = 16
    NUMBER_OF_RANDOM_PICS = 7

    def __init__(self):

        load_dotenv()
        self.token = os.getenv('TOKEN')
        self.bot = telebot.TeleBot(self.token, threaded=False)

        # Buttons
        self.button_get_info = types.KeyboardButton("Расскажи о себе!")
        self.button_who_am_i = types.KeyboardButton(r'🤔' + " Интересно.. Какой я сегодня котик?")
        self.button_start = types.KeyboardButton(" Покажи котика! ")
        self.button_continue = types.KeyboardButton(" Хочу ещё котиков! ")
        self.button_stop = types.KeyboardButton(" Спасибо! Хватит! ")

        # Keyboards
        self.keyboard_hello = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.keyboard_hello.add(self.button_get_info, self.button_start)

        self.keyboard_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.keyboard_start.add(self.button_who_am_i, self.button_start)

        self.keyboard_continue = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.keyboard_continue.add(self.button_continue, self.button_stop, self.button_who_am_i)

    def start_helper(self, message):
        """
        Greeting with user
        :param message: contains info about chat
        :return: None
        """
        start_message = "Привет! Если тебе плохо, я покажу тебе котиков. А если хорошо, тоже покажу"
        self.bot.send_message(message.chat.id, start_message, reply_markup=self.keyboard_hello)

    def send_kitty(self, message):
        """
        Sends random picture to user
        :param message: contains info about chat
        :return: None
        """
        file = str(random.randint(1, self.NUMBER_OF_RANDOM_PICS)) + '.jpeg'
        photo = 'https://storage.yandexcloud.net/kotiki/' + file
        self.bot.send_photo(message.chat.id, photo, reply_markup=self.keyboard_continue)

    def who_am_i(self, message):
        """
        Interaction with user
        :param message: contains info about chat
        :return: None
        """
        scanning = "Улыбнись! Идет сканирование ..."
        result = "Получилось! Сегодня ты похож(а) на этого котика!"
        self.bot.send_message(message.chat.id, scanning, reply_markup=self.keyboard_continue)
        self.bot.send_message(message.chat.id, result, reply_markup=self.keyboard_continue)
        file = str(random.randint(self.NUMBER_OF_RANDOM_PICS + 1, self.NUMBER_OF_PICS)) + '.jpeg'

        photo = 'https://storage.yandexcloud.net/kotiki/' + file
        self.bot.send_photo(message.chat.id, photo, reply_markup=self.keyboard_continue)

    def get_info(self, message):
        self.bot.send_message(message.chat.id, "Я умею показывать самых милых котиков!" + r'😾',
                              reply_markup=self.keyboard_hello)
        self.bot.send_message(message.chat.id, "Но не таких милых, как ты 🥺",
                              reply_markup=self.keyboard_hello)

    def finish(self, message):
        """Checkout to hello-stage buttons"""
        end_message = 'Пока! До скорого!'
        self.bot.send_message(message.chat.id, end_message, reply_markup=self.keyboard_hello)

    def reply_all_messages(self, message):
        """
        reply to any unexpected messages
        :param message:
        :return: None
        """
        self.bot.send_message(message.chat.id, "Я умею только котиков показывать " + r'😾',
                              reply_markup=self.keyboard_start)
    

cat_bot = Catbot()

def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    cat_bot.bot.process_new_updates([update])


@cat_bot.bot.message_handler(commands=['start'])
def start(message):
    cat_bot.start_helper(message)


@cat_bot.bot.message_handler(regexp="Интересно.. Какой я сегодня котик?")
def thinker(message):
    cat_bot.who_am_i(message)


@cat_bot.bot.message_handler(regexp="Расскажи о себе!")
def info(message):
    cat_bot.get_info(message)


@cat_bot.bot.message_handler(regexp="Покажи котика!")
def kitty(message):

    cat_bot.send_kitty(message)


@cat_bot.bot.message_handler(regexp="Хочу ещё котиков!")
def kitty(message):
    cat_bot.send_kitty(message)


@cat_bot.bot.message_handler(regexp="Спасибо! Хватит!")
def bot_finish(message):
    cat_bot.finish(message)


@cat_bot.bot.message_handler(content_types=["text"])
def repeat(message):
    cat_bot.reply_all_messages(message)
