import telebot
import datetime
import time
import threading
import requests

bot = telebot.TeleBot('Введите свой токен Бота')
first_rem = '09:00'
second_rem = '22:30'

reminders_active = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет, я буду напоминать тебе выпить таблетки каждое утро в 9:00 и ложиться спать в 10:30 \nЧтобы посмотреть что я могу еще нажми /help)')
    reminders_active[chat_id] = True
    reminder_thread = threading.Thread(target=send_reminders, args=(chat_id,))
    reminder_thread.start()

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '"/start" - Запустить напоминания, \n"/stop" - Остановить напоминания, \n"/timedata" - узнать, время, дату и день недели, \n"/weather" - узнать погоду')

@bot.message_handler(commands=['stop'])
def stop_message(message):
    chat_id = message.chat.id
    reminders_active[chat_id] = False
    bot.send_message(chat_id, 'Напоминания остановлены.')

@bot.message_handler(commands=['timedata'])
def time_data_message(message):
    now = datetime.datetime.now()
    time_data = now.strftime('%H:%M, %d %B %Y, %A')
    bot.send_message(message.chat.id, f'Текущее время: {time_data}')


@bot.message_handler(commands=['weather'])
def weather_command(message):

    OPENWEATHERMAP_API_KEY = 'API с сайта OPENWEATHERMAP'

    city_name = 'Ижевск'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=ru"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        weather_info = f"Температура в {city_name}: {temperature}°C\nОписание: {weather_description.capitalize()}"

        bot.send_message(message.chat.id, weather_info)
    else:
        bot.send_message(message.chat.id, 'Не удалось получить данные о погоде.')


def send_reminders(chat_id):
    while reminders_active.get(chat_id, False):
        now = datetime.datetime.now().strftime('%H:%M')
        if now == first_rem:
            bot.send_message(chat_id, 'Время выпить таблетки!')
            time.sleep(61)
        elif now == second_rem:
            bot.send_message(chat_id, 'Время ложиться спать!')
            time.sleep(61)
        time.sleep(1)

bot.polling(none_stop=True)