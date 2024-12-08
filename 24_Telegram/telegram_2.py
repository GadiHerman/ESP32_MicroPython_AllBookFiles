import utelegram
from machine import Pin
pin_led = Pin(2, mode=Pin.OUT)

def get_message(message):
    print('update_id: ',message['update_id'],'\n')
    print('-----------------------------------------------------------')  
    print('message/message_id: ',message['message']['message_id'],'\n')
    print('message/from: ',message['message']['from'],'\n')
    print('message/text: ',message['message']['text'],'\n')
    print('message/date: ',message['message']['date'],'\n')
    print('message/chat: ',message['message']['chat'],'\n')
    print('-----------------------------------------------------------')    
    print('message/chat/id: ',message['message']['chat']['id'],'\n')
    print('message/chat/last_name: ',message['message']['chat']['last_name'],'\n')
    print('message/chat/type: ',message['message']['chat']['type'],'\n')
    print('message/chat/first_name: ',message['message']['chat']['first_name'],'\n')
    print('-----------------------------------------------------------')
    bot.send(message['message']['chat']['id'], 'Type /on To turn on the light \nType  /off To turn off the light')

def led_on(message):
    print(message)
    pin_led.on()
    bot.send(message['message']['chat']['id'], 'The LED is on!')

def led_off(message):
    id = message['message']['chat']['id']
    print(id)
    pin_led.off()
    bot.send(id, 'The LED is off!')
    
bot = utelegram.ubot('7586682133:AAF5DwqgVzggB2kEkla8N2uAGtKdbovCdjA')
bot.register('/on', led_on)
bot.register('/off', led_off)
bot.set_default_handler(get_message)

print('BOT LISTENING')
bot.listen()

