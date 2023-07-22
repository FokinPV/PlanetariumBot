import requests
from datetime import datetime
from dateutil import parser
import telebot
import datetime
from telebot import types
from pprint import pprint
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

#events = []
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = 'jnekmkdk4jsjk2ms14b4ig5mpg@group.calendar.google.com'
calendar_work_id ='n8poc802qrffnos5clk79f9360@group.calendar.google.com'

TOKEN = 'INSERT_YOUR_TOKEN'
SHOW = {
    'hbm':'Обитаемая Луна',
    'cu':'Разноцветная вселенная',
    'jtss':'Путешествие по солнечной системе',
    'potu':'Призрак вселенной',
    'was':'Мы все Звёзды',
    'bope':'Рождение планеты земля',
    'gs':'Путеводные звёзды',
    'swwinter':'Времена года: Зима',
    'lq':'Загадка жизни',
    'moe':'Движение земли',
    'sim':'Небо в движении',
    'swspring':'Времена года: Весна',
    'bts':'Экзопланеты',
    'dino': 'Динозавры'
}

class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    calendar_id = 'jnekmkdk4jsjk2ms14b4ig5mpg@group.calendar.google.com'
    calendar_work_id ='n8poc802qrffnos5clk79f9360@group.calendar.google.com'
    time_now = datetime.datetime.now()
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename='deep-bivouac-374216-868699248eee.json', scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)


def time_parse_format_str(time):
    time_parse = parser.parse(time)
    real_time_start= (datetime.datetime(time_parse.year, time_parse.month, time_parse.day, time_parse.hour+3, time_parse.minute))
    real_time_str = real_time_start.strftime('%H:%M')
    return real_time_str

def get_worker_today():
    while True:
        worker = []
        time_now = datetime.datetime.now()
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute)).isoformat() + 'Z'
        tomorrow = time_now + datetime.timedelta(days=1)
        end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_work_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=2, timeZone="UTC").execute()
        for event in events['items']:
            worker.append(event['summary'])
        if 'БЗЗ: Николай Рязанов' in worker:
            return 'Сегодня в БЗЗ Дмитрий Насонов\n +79164851698\n @almucantar'
        else:
            return 'Сегодня в БЗЗ Павел Фокин\n +79253095006\n @fokinview'

def get_today_events_from_google():
    page_token = ''
    list_event = []
    try:
        time_now = datetime.datetime.now();
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute)).isoformat() + 'Z'
        tomorrow = time_now + datetime.timedelta(days=1)
        end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=10, timeZone="UTC").execute()
        while True:
            for event in events['items']:
                event_name = event['summary']
                event_start_time = event['start']['dateTime']
                event_end_time = event['end']['dateTime']
                real_time_est_str = time_parse_format_str(event_start_time)
                real_time_eet_str = time_parse_format_str(event_end_time)
                all_time = f'{real_time_est_str}-{real_time_eet_str}'
                list_event.append(f'{all_time} : {event_name}')
            if not page_token:
                break
            if not events['items']:
                print('No upcoming events found.')
                return 'Сегодня шоу больше нет'
        return list_event

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_data_from_google():
    page_token = ''
    try:
        time_now = datetime.datetime.now();
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute)).isoformat() + 'Z'
        time_now_correct = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour+3, time_now.minute))
        tomorrow = time_now + datetime.timedelta(days=1)
        end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=2, timeZone="UTC").execute()
        while True:
            for event in events['items']:
                event_name = event['summary']
                event_start_time = event['start']['dateTime']
                d = parser.parse(event_start_time)
                real_time = (datetime.datetime(d.year, d.month, d.day, d.hour+3, d.minute))
                real_time_str = real_time.strftime('%H:%M')
                if real_time > time_now_correct:
                    print(f'{real_time} > {time_now}')
                    print(event['summary'], event['start']['dateTime'])
                    return f'{event_name}\nНачало в {real_time_str}'
                page_token = event.get('nextPageToken')
            if not page_token:
                break
            if not events['items']:
                print('No upcoming events found.')
                return 'Сегодня шоу больше нет'

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_data():
    req = requests.get("https://91.229.###.###/api/narrations")
    response = req.json()
    sell_price = response["show_name"]["end_time_ms"]


def telegram_bot(token):
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands=["start"])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        show = types.KeyboardButton("Show")
        today = types.KeyboardButton("Today")
        worker = types.KeyboardButton("Employee")
        markup.row(show, today, worker)
        bot.send_message(message.chat.id, f"Добро пожаловать в бот сервис БЗЗ.\nНабери show для того чтобы узнать время окончания.\nКоманда today покажет расписание на день.\n Команда Employee подскажет кто сегодня в правит БЗЗ.",reply_markup=markup)

    @bot.message_handler()
    def send_text(message):
        time = datetime.datetime.now()
        real_time= (datetime.datetime(time.year, time.month, time.day, time.hour+3, time.minute))
        real_time_str = real_time.strftime('%H:%M')
        if message.text.lower() == "show":
            try:
                google_results = get_data_from_google()
                req = requests.get("http://91.229.###.###/api/narrations")
                print(req)
                if req.status_code == 200:
                    response = req.json()
                    show_name = response["show_name"]
                    show_end = float(response["end_time_ms"])
                    time = show_end/1000
                    dt_object = datetime.datetime.fromtimestamp(time)
                    dt_real_time= (datetime.datetime(dt_object.year, dt_object.month, dt_object.day, dt_object.hour+3, dt_object.minute, dt_object.second))
                    dt_real_time_str = dt_real_time.strftime('%H:%M:%S')
                    if google_results != None:
                        bot.send_message(
                            message.chat.id,
                            f"Текущее время: {real_time_str}\n\nТекущее шоу: {SHOW[show_name]}\nВремя окончания: {dt_real_time_str}\n\nСледующее шоу:\n{google_results}"
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            f"Текущее время: {real_time_str}\n\nТекущее шоу: {SHOW[show_name]}\nВремя окончания: {dt_real_time_str}\n\nНа сегодня всё!"
                        )
                else:
                    if google_results != None:
                        bot.send_message(
                            message.chat.id,
                            f"В БЗЗ перерыв.\n\nСледующее шоу - {google_results}"
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            f"На сегодня всё!"
                        )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Упс... Что-то пошло не так..."
                )
        elif message.text.lower() == "today":
            result = get_today_events_from_google()
            results = "\n".join(result)
            bot.send_message(
                message.chat.id,
                f"Текущее время: {real_time_str}\n\n{results}"
            )
        elif message.text.lower() == "employee":
            bot.send_message(
                message.chat.id,
                f"{get_worker_today()}"
            )
        else:
            bot.send_message(message.chat.id, "Вы ввели несуществующую команду!")
    while True:
        try:
            bot.polling()
        except:
            continue

if __name__ == '__main__':
    obj = GoogleCalendar()
    telegram_bot(TOKEN)
    
