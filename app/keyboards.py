from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)




btn_calendar_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Сегодня", callback_data="calendar_today"),
            InlineKeyboardButton(text="📅 Завтра", callback_data="calendar_tomorrow"),
            InlineKeyboardButton(text="📅 На неделе", callback_data="calendar_week")
        ]
    ])


def create_stars_keyboard(period: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"three_stars_{period}"),
            InlineKeyboardButton(text="⭐⭐", callback_data=f"two_stars_{period}"),
            InlineKeyboardButton(text="⭐", callback_data=f"star_{period}"), 
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_calendar")
        ]
    ])

# Создание клавиатур
btn_sort_by_stars_today = create_stars_keyboard("today")
btn_sort_by_stars_tomorrow = create_stars_keyboard("tomorrow")
btn_sort_by_stars_week = create_stars_keyboard("week")


def get_back_button(period: str) -> InlineKeyboardMarkup:
    """Создает кнопку 'Назад' для указанного периода"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_to_{period}")]
    ])


btn_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Котировки')],
    [KeyboardButton(text='Экономический календарь')]
    
],
                        resize_keyboard=True)


