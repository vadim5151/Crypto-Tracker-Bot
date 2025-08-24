from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message,CallbackQuery

import app.keyboards as kb
from services.crypto_price import get_crypto_data
from utils.formatters import *
from services.news_parser import fetch_economic_calendar



router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello', reply_markup=kb.btn_main)


@router.message(F.text == 'Котировки')
async def get_crypto_price(message: Message):
    btc_info = await get_crypto_data('bitcoin')  
    eth_info = await get_crypto_data('ethereum')
    ton_info = await get_crypto_data('the-open-network')
    
    formatted_message = format_crypto_prices({'₿ <b>Bitcoin</b> (BTC)': btc_info, 
                                              '⟠ <b>Ethereum</b> (ETH)': eth_info, 
                                              '₮ <b>Toncoin</b> (TON)': ton_info}) 
    await message.answer(formatted_message, parse_mode="HTML")


@router.message(F.text == 'Экономический календарь')
async def get_part_news(message: Message):
    today_events, tomorrow_events = await fetch_economic_calendar()

    event = format_daily(today_events, tomorrow_events)
    await message.answer(
        event,
        parse_mode="HTML",
        reply_markup=kb.get_calendar_keyboard()
        )
    

@router.callback_query(F.data == 'calendar_today')
async def get_today_news(callback: CallbackQuery):
    today_events, _ = await fetch_economic_calendar()
    
    message_parts = format_events_today(today_events)

    for i, part in enumerate(message_parts):
        if i == len(message_parts) - 1:
            await callback.message.answer(part, parse_mode="HTML", reply_markup=kb.get_back_keyboard())
        else:
            await callback.message.answer(part, parse_mode="HTML")
    
    await callback.answer('')


@router.callback_query(F.data == 'calendar_tomorrow')
async def get_tomorrow_news(callback: CallbackQuery):
    _, tomorrow_events = await fetch_economic_calendar()
    
    message_parts = format_events_tomorrow(tomorrow_events)

    for i, part in enumerate(message_parts):
        if i == len(message_parts) - 1:
            await callback.message.answer(part, parse_mode="HTML", reply_markup=kb.get_back_keyboard())
        else:
            await callback.message.answer(part, parse_mode="HTML")
    
    await callback.answer('')


