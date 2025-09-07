from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
from utils.formatters.crypto_formatters import format_crypto_prices
from database.requests import get_coins



router = Router()


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