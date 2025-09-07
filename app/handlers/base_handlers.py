from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


import app.keyboards as kb



router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! Выберите опцию:', reply_markup=kb.btn_main)