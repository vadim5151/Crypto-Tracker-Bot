# run.py
import asyncio
import signal
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TG_TOKEN
from app.handlers import router
from database.models import create_tables, drop_database
from services.news_parser import fetch_economic_calendar
from database.requests import save_events_to_db

bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def shutdown(signal, loop):
    """Корректное завершение работы приложения"""
    print(f"Получен сигнал {signal.name}. Завершение работы...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def main():
    """Основная функция запуска приложения"""
    await create_tables()
    dp.include_router(router)
    
    # Запускаем бота и парсинг одновременно
    bot_task = asyncio.create_task(dp.start_polling(bot))
    parsing_task = asyncio.create_task(scheduled_parsing_news())
    
    # Ожидаем завершения обеих задач
    await asyncio.gather(bot_task, parsing_task)


async def scheduled_parsing_news():
    """Функция для периодического парсинга"""
    while True:
        try:
            print(f"{datetime.now()}: Запуск планового парсинга...")
            
            # Очищаем базу данных перед новым парсингом
            await drop_database()
            print("База данных очищена")
            
            # Создаем таблицы заново
            await create_tables()
            print("Таблицы созданы заново")
            
            # Парсим события
            events = await fetch_economic_calendar()
            if events:
                saved_count = await save_events_to_db(events)
                print(f"Парсинг завершен. Сохранено событий: {saved_count}")
            else:
                print("Парсинг завершен. Событий не найдено.")
            
            # Ожидание 12 часов до следующего запуска
            print("Ожидание 12 часов до следующего запуска...")
            await asyncio.sleep(12 * 60 * 60)
        except asyncio.CancelledError:
            print("Парсинг отменен")
            raise
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            # Ожидание 1 часа при ошибке
            await asyncio.sleep(60 * 60)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    # Настройка обработки сигналов для корректного завершения
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

   
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop))
        )
    
    try:
        # Для однократного запуска
        # results = loop.run_until_complete(main())
        
        # Для периодического запуска (раскомментируйте следующую строку)
        loop.run_until_complete(scheduled_parsing_news())
 

    finally:
        loop.close()
    