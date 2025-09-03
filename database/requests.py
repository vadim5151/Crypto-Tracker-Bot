from datetime import datetime, UTC, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert



from database.models import async_session, News, Coin



from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, update
from contextlib import asynccontextmanager


async def save_events_to_db(events_data):
    if not events_data:
        return 0

    async with async_session() as session:
        try:
            for period_name, events_list in events_data.items():
                for event_data in events_list:
                    event_id = event_data.get('id')
                    if not event_id:
                        continue

                    # Создаем statement для вставки с обработкой конфликта
                    stmt = insert(News).values(
                        event_id=event_id,
                        event_date=event_data.get('date'),
                        event_time=event_data.get('time'),
                        currency=event_data.get('currency'),
                        importance=event_data.get('importance'),
                        event_name=event_data.get('title'),
                        actual=event_data.get('actual'),
                        forecast=event_data.get('forecast'),
                        previous=event_data.get('prev'),
                        update_at=datetime.now(UTC).replace(tzinfo=None)
                    ).on_conflict_do_nothing(index_elements=['event_id'])

                    await session.execute(stmt)

            await session.commit()
            print("Данные успешно сохранены")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка: {e}")

 
async def get_today_events():
    async with async_session() as session:
        all_events = []

        today_datetime = datetime.now()
        today_date_str = today_datetime.strftime("%Y/%m/%d")
        
        formatted_date = today_date_str
        
        result = await session.execute(
            select(News).where(News.event_date == formatted_date)
            )
        events = result.scalars().all()

        for event in events:
            all_events.append({
                'event_time': event.event_time,
                'currency': event.currency,
                'importance': event.importance,
                'event_name': event.event_name,
                'actual': event.actual,
                'forecast': event.forecast,
                'prev': event.previous,
                'update_at': event.update_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return all_events
    

async def get_tomorrow_events():
    async with async_session() as session:
        all_events = []

        tomorrow_datetime = datetime.now() + timedelta(days=1)
        tomorrow_date_str = tomorrow_datetime.strftime("%Y/%m/%d")
        
        formatted_date = tomorrow_date_str

        result = await session.execute(
            select(News).where(News.event_date == formatted_date)
        )
        events = result.scalars().all()

        for event in events:
            all_events.append({
                'event_time': event.event_time,
                'currency': event.currency,
                'importance': event.importance,
                'event_name': event.event_name,
                'actual': event.actual,
                'forecast': event.forecast,
                'prev': event.previous,
                'update_at': event.update_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return all_events


async def get_week_events():
    async with async_session() as session:
        all_events = []

        result = await session.execute(select(News))
        events = result.scalars().all()

        for event in events:
            all_events.append({
                'event_date': event.event_date,
                'event_time': event.event_time,
                'currency': event.currency,
                'importance': event.importance,
                'event_name': event.event_name,
                'actual': event.actual,
                'forecast': event.forecast,
                'prev': event.previous,
                'update_at': event.update_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return all_events


async def save_coins_to_bd(top_coins, top_gainers, top_losers):
    async with async_session() as session:
        all_coins = top_coins+top_gainers+top_losers
        try:
            for coin in all_coins:
                top_coins_data = {
                    'rank_type': coin['rank_type'],
                    'ticker':coin['ticker'],
                    'name': coin['name'],
                    'market_cup': coin['market_cup'].replace('\\u202', ''),
                    'price_change_24hm': coin['change_price'],
                    'price': coin['price']
                }
                            
                # Создаем новое событие
                new_event = Coin(**top_coins_data)
                session.add(new_event)
                 
            await session.commit()
            print(f"Успешно сохраненны монеты")
            return 0
                        
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при сохранении в БД: {e}")
            import traceback
            traceback.print_exc()
            return 0
        

async def get_coins(rank_type):
    async with async_session() as session:
        coins_data = []

        result = await session.execute(
            select(Coin).where(Coin.rank_type == rank_type)
            )
            
        top_coins = result.scalars().all()

        for coin in top_coins:
            coins_data.append({
                'ticker': coin.ticker,
                'name': coin.name,
                'price': coin.price,
                'market_cup': coin.market_cup,
                'price_change_24hm': coin.price_change_24hm,
                'update_at': coin.update_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return coins_data


