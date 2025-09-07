from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)



btn_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Котировки')],
    [KeyboardButton(text='Экономический календарь')]
    
],
                        resize_keyboard=True)


btn_calendar_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Сегодня", callback_data="calendar_today"),
            InlineKeyboardButton(text="📅 Завтра", callback_data="calendar_tomorrow"),
            InlineKeyboardButton(text="📅 На неделе", callback_data="calendar_week")
        ]
    ])


def create_main_calendar_keyboard(period: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Предыдущая страница", callback_data="prev_events"),
            InlineKeyboardButton(text="Следующая страница ▶️", callback_data="more_events")
        ],
        [
            InlineKeyboardButton(text="◀️ Назад к календарю", callback_data="back_to_calendar")
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"three_stars_{period}"),
            InlineKeyboardButton(text="⭐⭐", callback_data=f"two_stars_{period}"),
            InlineKeyboardButton(text="⭐", callback_data=f"star_{period}")
        ]
    ])


btn_sort_by_stars_today = create_main_calendar_keyboard("today")
btn_sort_by_stars_tomorrow = create_main_calendar_keyboard("tomorrow")
btn_sort_by_stars_week = create_main_calendar_keyboard("week")


def get_btn_events_both(period: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Предыдущая страница", callback_data="prev_events"),
            InlineKeyboardButton(text="Следующая страница ▶️", callback_data="more_events")
        ],
        [
            InlineKeyboardButton(text="◀️ Назад к календарю", callback_data="back_to_calendar")
        ]
    ])


btn_sort_coins = InlineKeyboardMarkup(inline_keyboard=[
        
            [InlineKeyboardButton(text="Топ монет по капитализации", callback_data="opt_top_coin")],
            [InlineKeyboardButton(text="Топ по росту", callback_data="opt_gainer")],
            [InlineKeyboardButton(text="Топ монет по падению", callback_data="opt_loser")]
        
    ])


btn_coins_more = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="◀️ Назад", callback_data="prev_coins"),
        InlineKeyboardButton(text="Еще", callback_data="more_coins")
    ],
    [
        InlineKeyboardButton(text="◀️ В меню", callback_data="back_to_quotes")
    ]
])

btn_coins_no_more = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="◀️ Назад", callback_data="prev_coins")
    ],
    [
        InlineKeyboardButton(text="◀️ В меню", callback_data="back_to_quotes")
    ]
])
