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


def create_stars_keyboard(period: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text="◀️ Назад", callback_data="prev_events"),
        InlineKeyboardButton(text="Еще ▶️", callback_data="more_events")
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


btn_sort_by_stars_today = create_stars_keyboard("today")
btn_sort_by_stars_tomorrow = create_stars_keyboard("tomorrow")
btn_sort_by_stars_week = create_stars_keyboard("week")


def get_back_button(period: str) -> InlineKeyboardMarkup:
    """Создает кнопку 'Назад' для указанного периода"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_to_{period}")]
    ])


btn_events_more = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Еще ▶️", callback_data="more_events")
    ],
    [
        InlineKeyboardButton(text="◀️ Назад к календарю", callback_data="back_to_calendar")
    ]
])

btn_events_prev_only = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="◀️ Назад", callback_data="prev_events")
    ],
    [
        InlineKeyboardButton(text="◀️ Назад к календарю", callback_data="back_to_calendar")
    ]
])

btn_events_both = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="◀️ Назад", callback_data="prev_events"),
        InlineKeyboardButton(text="Еще ▶️", callback_data="more_events")
    ],
    [
        InlineKeyboardButton(text="◀️ Назад к календарю", callback_data="back_to_calendar")
    ]
])

btn_events_back_only = InlineKeyboardMarkup(inline_keyboard=[
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
