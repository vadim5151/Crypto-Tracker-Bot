from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from utils.formatters import *
from database.requests import get_today_events, get_tomorrow_events, get_week_events
from database.requests import get_coins



class CryptoState(StatesGroup):
    waiting_for_more = State()



router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello', reply_markup=kb.btn_main)


@router.message(F.text == 'Котировки')
async def get_crypto_price(message: Message):
    await message.answer('Какие монеты хотите посмотреть?', reply_markup=kb.btn_sort_coins)


@router.callback_query(F.data.startswith('opt_'))
async def get_coins_handlers(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    action = callback.data[4:]

    coins_data = await get_coins(action)

    await state.update_data(
        coins_data=coins_data,
        offset=0,
        action=action
    )

    message = format_crypto_prices(coins_data, offset=0, limit=20)
    
    await callback.message.answer(message, parse_mode="HTML", reply_markup=kb.btn_coins_more)
    await callback.answer('')


@router.callback_query(F.data == 'more_coins')
async def get_more_coins(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coins_data = data.get('coins_data', [])
    current_offset = data.get('offset', 0)

    new_offset = current_offset + 20
    
    if new_offset >= len(coins_data):
        await callback.answer("Больше нет монет для показа")
        return 0
    
    message = format_crypto_prices(coins_data, offset=new_offset, limit=20)
    
    await state.update_data(offset=new_offset)
    
    await callback.message.edit_text(message, parse_mode="HTML", reply_markup=kb.btn_coins_more)
    await callback.answer('')


@router.callback_query(F.data == 'prev_coins')
async def get_prev_coins(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coins_data = data.get('coins_data', [])
    current_offset = data.get('offset', 0)

    new_offset = current_offset - 20

    if new_offset < 0:
        await callback.answer("Это первая страница")
        return 0
    
    message = format_crypto_prices(coins_data, offset=new_offset, limit=20)

    await state.update_data(offset=new_offset)

    await callback.message.edit_text(message, parse_mode="HTML", reply_markup=kb.btn_coins_more)
    await callback.answer('')


@router.callback_query(F.data == 'back_to_quotes')
async def get_crypto_price(callback: CallbackQuery):
    await callback.message.edit_text('Какие монеты хотите посмотреть?', reply_markup=kb.btn_sort_coins)


@router.message(F.text == 'Экономический календарь')
async def get_part_news(message: Message):
    await message.answer('На какой день хотите посмотреть события', reply_markup=kb.btn_calendar_keyboard)
    

@router.callback_query(F.data == 'calendar_today')
async def get_today_news(callback: CallbackQuery, state: FSMContext):
    today_events = await get_today_events()
    print(f"Событий на сегодня: {len(today_events)}")

    await state.update_data(
        events=today_events,
        offset=0,
        period="today",
        importance=None
    )

    message_parts = format_events_today(today_events, limit=20)  # Теперь возвращает список частей

    # Отправляем первую часть сообщения с клавиатурой
    if message_parts:
        

        # Отправляем первую часть
        await callback.message.answer(message_parts[0], parse_mode="HTML", reply_markup=kb.btn_sort_by_stars_today)

        # Если есть еще части, отправляем их без клавиатуры
        for part in message_parts[1:]:
            await callback.message.answer(part, parse_mode="HTML")
    else:
        await callback.message.answer("Нет данных для отображения.", reply_markup=kb.btn_events_back_only)

    await callback.answer()


@router.callback_query(F.data == 'calendar_tomorrow')
async def get_tomorrow_news(callback: CallbackQuery, state: FSMContext):
    tomorrow_events = await get_tomorrow_events()

    await state.update_data(
        events=tomorrow_events,
        offset=0,
        period="today",
        importance=None
    )

    message_parts = format_events_tomorrow(tomorrow_events, limit=20)

    if message_parts:
    
        await callback.message.answer(message_parts[0], parse_mode="HTML", reply_markup=kb.btn_sort_by_stars_tomorrow)

        for part in message_parts[1:]:
            await callback.message.answer(part, parse_mode="HTML")
    else:
        await callback.message.answer("Нет данных для отображения.", reply_markup=kb.btn_events_back_only)

    await callback.answer()


@router.callback_query(F.data == 'calendar_week')
async def get_week_news(callback: CallbackQuery, state: FSMContext):
    week_events = await get_week_events()
    
    await state.update_data(
        events=week_events,
        offset=0,
        period="today",
        importance=None
    )

    message_parts = format_events_today(week_events, limit=20)  # Теперь возвращает список частей

    if message_parts:

        await callback.message.answer(message_parts[0], parse_mode="HTML", reply_markup=kb.btn_sort_by_stars_week)

        # Если есть еще части, отправляем их без клавиатуры
        for part in message_parts[1:]:
            await callback.message.answer(part, parse_mode="HTML")
    else:
        await callback.message.answer("Нет данных для отображения.", reply_markup=kb.btn_events_back_only)

    await callback.answer()


@router.callback_query(F.data == 'more_events')
async def get_more_events(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    events = data.get('events', [])
    current_offset = data.get('offset', 0)
    period = data.get('period', '')
    importance = data.get('importance')

    new_offset = current_offset + 20
    
    if new_offset >= len(events):
        await callback.answer("Больше нет событий для показа")
        return
    
    # Форматируем события в зависимости от периода и важности
    if importance:
        if period == "today":
            message = sort_today_events(events, importance, new_offset, 20)
        elif period == "tomorrow":
            message = sort_tomorrow_events(events, importance, new_offset, 20)
        else:
            message = sort_week_events(events, importance, new_offset, 20)
    else:
        if period == "today":
            message_parts = format_events_today(events, new_offset, 20)
        elif period == "tomorrow":
            message_parts = format_events_tomorrow(events, new_offset, 20)
        else:
            message_parts = format_events_week(events, new_offset, 20)
        message = message_parts[0] if message_parts else "Нет событий"
    
    await state.update_data(offset=new_offset)
    
    # Проверяем, есть ли еще события
    if new_offset + 20 < len(events):
        reply_markup = kb.btn_events_both
    else:
        reply_markup = kb.btn_events_prev_only
    
    await callback.message.edit_text(message, parse_mode="HTML", reply_markup=reply_markup)
    await callback.answer('')


@router.callback_query(F.data == 'prev_events')
async def get_prev_events(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    events = data.get('events', [])
    current_offset = data.get('offset', 0)
    period = data.get('period', '')
    importance = data.get('importance')

    new_offset = current_offset - 20
    
    if new_offset < 0:
        await callback.answer("Это первая страница")
        return
    
    # Форматируем события в зависимости от периода и важности
    if importance:
        if period == "today":
            message = sort_today_events(events, importance, new_offset, 20)
        elif period == "tomorrow":
            message = sort_tomorrow_events(events, importance, new_offset, 20)
        else:
            message = sort_week_events(events, importance, new_offset, 20)
    else:
        if period == "today":
            message_parts = format_events_today(events, new_offset, 20)
        elif period == "tomorrow":
            message_parts = format_events_tomorrow(events, new_offset, 20)
        else:
            message_parts = format_events_week(events, new_offset, 20)
        message = message_parts[0] if message_parts else "Нет событий"
    
    await state.update_data(offset=new_offset)
    
    # Проверяем, есть ли еще события
    if new_offset == 0:
        reply_markup = kb.btn_events_more
    else:
        reply_markup = kb.btn_events_both
    
    await callback.message.edit_text(message, parse_mode="HTML", reply_markup=reply_markup)
    await callback.answer('')


@router.callback_query(F.data == 'back_to_calendar')
async def back_to_calendar(callback: CallbackQuery):
    await callback.message.answer('На какой день хотите посмотреть события', reply_markup=kb.btn_calendar_keyboard)


STARS_HANDLERS = {
    "three_stars_today": (3, "today"),
    "two_stars_today": (2, "today"),
    "star_today": (1, "today"),
    "three_stars_tomorrow": (3, "tomorrow"),
    "two_stars_tomorrow": (2, "tomorrow"),
    "star_tomorrow": (1, "tomorrow"),
    "three_stars_week": (3, "week"),
    "two_stars_week": (2, "week"),
    "star_week": (1, "week"),
}

@router.callback_query(F.data.in_(STARS_HANDLERS.keys()))
async def handle_all_stars_filters(callback: CallbackQuery, state: FSMContext):
    importance, period = STARS_HANDLERS[callback.data]
    
    if period == "today":
        events = await get_today_events()
    elif period == "tomorrow":
        events = await get_tomorrow_events()
    else:
        events = await get_week_events()
    
    # Фильтруем события по важности
    filtered_events = [event for event in events if event['importance'] == importance]
    
    # Сохраняем отфильтрованные события в состоянии
    await state.update_data(
        events=events,
        offset=0,
        period=period,
        importance=importance
    )
    
    # Форматируем сообщение
    if period == "today":
        message = sort_today_events(filtered_events, importance, 0, 20)
    elif period == "tomorrow":
        message = sort_tomorrow_events(filtered_events, importance, 0, 20)
    else:
        message = sort_week_events(filtered_events, importance, 0, 20)
    
    # Проверяем, есть ли еще события
    if len(filtered_events) > 20:
        reply_markup = kb.btn_events_more
    else:
        reply_markup = kb.get_back_button(period)
    
    await callback.message.answer(message, parse_mode="HTML", reply_markup=reply_markup)
    await callback.answer('')



@router.callback_query(F.data.startswith("back_to_"))
async def handle_back_button(callback: CallbackQuery, state: FSMContext):
    # Извлекаем период из callback_data
    period = callback.data.replace("back_to_", "")
    
    # В зависимости от периода вызываем соответствующий обработчик
    if period == "today":
        await get_today_news(callback, state)
    elif period == "tomorrow":
        await get_tomorrow_news(callback, state)
    elif period == "week":
        await get_week_news(callback, state)
    else:
        await callback.answer("Ошибка при нажатии кнопки назад")