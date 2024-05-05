import telebot
from telebot import types
import threading
import json
import schedule
import jsonpickle

from time import sleep
from timer import Timer


bot = telebot.TeleBot('6941527127:AAFWTmtSzMa7O8nthEK6enpqcfp8zGaIXWI')

def save_stats():
    global Timers
    with open("database.json", "w") as datafile:
        data = jsonpickle.encode(Timers)
        datafile.write(data)
        #print(Timers)
    print("Data saved!")


def load_stats():
    global Timers
    with open("database.json", "r") as datafile:
        data = datafile.read()
        Timers = jsonpickle.decode(data)
        #print(data)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
    sleep = types.KeyboardButton("Сон")
    univteach = types.KeyboardButton("Университет")
    OnWay = types.KeyboardButton("В пути")
    Games = types.KeyboardButton("Игры")
    SelfStudy = types.KeyboardButton("Самообучение")
    Other = types.KeyboardButton("Остальное")
    Stats = types.KeyboardButton("Статистика")
    keys = [sleep, univteach, OnWay, Games, SelfStudy, Other, Stats]
    for key in keys:
        keyboard.add(key)

    global Timers
    Timers[f'{m.chat.id}'] =  Timer()

    bot.send_message(m.chat.id, "Привет, нажми то ,чем сейчас занимаешься", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        global Timers
        #print("Timers ", Timers)
        if message.text.strip() == "Сон":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("Сон")
            answer = f"Отсчет начат, спокойной ночи!"

        elif message.text.strip() == "Университет":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("Университет")
            answer = "Отсчет начат, удачной учебы!"

        elif message.text.strip() == "В пути":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("В пути")
            answer = "Отсчет начат, удачной дороги!"

        elif message.text.strip() == "Игры":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("Игры")
            answer = "Отсчет начат, удачной катки!"

        elif message.text.strip() == "Самообучение":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("Самообучение")
            answer = "Отсчет начат, самообучение - важно!"

        elif message.text.strip() == "Остальное":
            q = Timers[f'{message.chat.id}'].StopCase()
            Timers[f'{message.chat.id}'].StartCase("Остальное")
            answer = "Отсчет начат, остальное тоже важно!"

        elif message.text.strip() == "Статистика":
            answer = str(Timers[f'{message.chat.id}'])

        else:
            answer = "Введите валидное действие"
        #print(str(Timers[message.chat.id]))
        bot.send_message(message.chat.id, answer)
    except KeyError:
        bot.send_message(message.chat.id, "Сначала нажми start!")

Timers = {}
try:
    load_stats()
except:
    print("Load error!")
savet = threading.Thread(target=bot.infinity_polling, daemon=True).start()
schedule.every(10).seconds.do(save_stats).tag("saving")
while True:
    schedule.run_pending()
    sleep(1)