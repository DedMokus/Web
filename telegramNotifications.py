import telebot


token = "6941527127:AAFWTmtSzMa7O8nthEK6enpqcfp8zGaIXWI"
bot = telebot.TeleBot(token)


chatID = -1002069870365
text = "hello"

def sendNotification(text):
    bot.send_message(chat_id=chatID, text=text)
    return 0
