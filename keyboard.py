from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_add_words = KeyboardButton('Добавить слова')
button_learn_words = KeyboardButton('Учить слова')
button_cancel = KeyboardButton('Отмена')
button_lat_ru = KeyboardButton('Слово - перевод')
button_ru_lat = KeyboardButton('Перевод - слово')

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

start_keyboard.add(button_learn_words)
start_keyboard.add(button_add_words)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

cancel_keyboard.add(button_cancel)

learn_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

learn_keyboard.add(button_lat_ru)
learn_keyboard.add(button_ru_lat)