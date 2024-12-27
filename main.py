import yt_dlp
import telebot
from telebot import types
import os
import requests
 

bot = telebot.TeleBot('')

telebot.apihelper.SESSION = requests.Session()
telebot.apihelper.SESSION.timeout = 1201
telebot.apihelper.READ_TIMEOUT = 1200

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('TikTok')
    btn2 = types.KeyboardButton('Instagram')
    btn3 = types.KeyboardButton('YouTube')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Hello, this bot can download videos from Instagram, YouTube, and TikTok.', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'TikTok':
        bot.send_message(message.chat.id, 'Send the link to the TikTok video.')
    elif message.text == 'Instagram':
        bot.send_message(message.chat.id, 'Send the link to the Instagram video.')
    elif message.text == 'YouTube':
        bot.send_message(message.chat.id, 'Send the link to the YouTube video.')
    elif message.text.startswith(('http://', 'https://')):  # Check if the message is a link
        get_link(message)
    else:
        bot.send_message(message.chat.id, 'Please send a valid link.')

def get_link(message):
    link = message.text
    ydl_opts = {
        'continuedl': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'n_threads': 10,
        'http_chunk_size': 10485760,
        'socket_timeout': 120,
    }

    try:
        # Send a loading message and save its ID
        loading_message = bot.send_message(message.chat.id, "Downloading, please wait...")

        os.makedirs('downloads', exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info_dict)

        with open(video_file, 'rb') as video:
            bot.send_video(message.chat.id, video)

        # Delete the loading message
        bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

        # Send a message indicating the download is complete
        bot.send_message(message.chat.id, 'Download complete!')

        os.remove(video_file)
    except Exception as e:
        bot.send_message(message.chat.id, f'An error occurred: {str(e)}')

bot.polling()
