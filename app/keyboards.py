from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)




def get_calendar_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Сегодня", callback_data="calendar_today"),
            InlineKeyboardButton(text="📅 Завтра", callback_data="calendar_tomorrow")
        ]
    ])


btn_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Котировки')],
    [KeyboardButton(text='Экономический календарь')]
    
],
                        resize_keyboard=True)

