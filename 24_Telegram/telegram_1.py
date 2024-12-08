import utelegram

def get_message(message):
    print(message)
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())

def reply_ping(message):
    print(message)
    bot.send(message['message']['chat']['id'], 'pong')

bot = utelegram.ubot('7586682133:AAF5DwqgVzggB2kEkla8N2uAGtKdbovCdjA')
bot.register('/ping', reply_ping)
bot.set_default_handler(get_message)

print('BOT LISTENING')
bot.listen()
