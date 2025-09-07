from datetime import datetime



def format_event(event):
    time = event['event_time']
    currency = event['currency']
    stars = '★' * event['importance']
    event_name = event['event_name']
    actual = event['actual']
    forecast = event['forecast']
    prev = event['prev']
    
    # Добавляем дату, если она есть в событии
    date_str = ''
    if 'event_date' in event and event['event_date']:
        date_str = f" ({event['event_date']})"
   
    return (
        f'''⏰ <b>{time}</b>{date_str}
   🏦 Валюта: {currency}
   ⭐ Важность: {stars}
   📊 Событие: {event_name}
   📈 Прогноз: {forecast} | Пред.: {prev}
        '''
    )

def format_daily(today_events, tomorrow_events):
    current_time = datetime.now().strftime("%H:%M")
    
    text = f"📊 <b>Экономический календарь</b> (обновлено {current_time})\n\n"
    
    if today_events and today_events[0] != 'Событий не запланировано':
        text += f"📅 <b>Сегодня:</b> {len(today_events)} событий\n"

        important_today = [event for event in today_events if event['stars'] >= 2][:3]

        for event in important_today:
            text += f"• {format_event(event)}\n"
        text += "\n"

    else:
        text += "📅 <b>Сегодня:</b> нет событий\n\n"
    
    if tomorrow_events and tomorrow_events[0] != 'Событий не запланировано':
        text += f"📅 <b>Завтра:</b> {len(tomorrow_events)} событий\n"

        important_tomorrow =[event for event in tomorrow_events if event['stars'] >= 2][:3]

        for event in important_tomorrow:
            text += f"• {format_event(event)}\n"
    else:
        text += "📅 <b>Завтра:</b> нет событий"
    
    return text+'...\n Посмотреть больше событий'

def split_text(text: str, max_length: int = 4096) -> list[str]:
    """
    Разбивает текст на части заданной максимальной длины.
    Старается разбивать по переносам строк, чтобы не обрывать предложения.
    """
    if len(text) <= max_length:
        return [text]

    parts = []
    while text:
        # Если оставшийся текст уже короткий
        if len(text) <= max_length:
            parts.append(text)
            break

        # Находим место для раздела: последний перенос строки в пределах лимита
        split_index = text.rfind('\n', 0, max_length)
        # Если не нашли перенос, делим по границе символа
        if split_index == -1:
            split_index = max_length

        part = text[:split_index]
        parts.append(part)
        text = text[split_index:].lstrip()  # Убираем ведущие пробелы с начала новой части

    return parts


def format_events_today(events, offset=0, limit=20, max_length=4096):
    if not events:
        return ["📅 <b>На сегодня:</b> нет событий"]

    events_to_show = events[offset:offset + limit]
    if not events_to_show:
        return ["Больше нет событий для показа"]

    update_at = events_to_show[0]['update_at']
    base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    base_text += f"📅 <b>Сегодня:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)}\n\n"

    event_texts = []
    for event in events_to_show:
        event_str = f"• {format_event(event)}\n"
        event_texts.append(event_str)

    # Собираем все тексты событий в один большой текст
    full_text = base_text + "".join(event_texts)

    # Разбиваем на части, если необходимо
    return split_text(full_text, max_length)


def format_events_tomorrow(events, offset=0, limit=20, max_length=4096):
    if not events:
        return ["📅 <b>На завтра:</b> нет событий"]

    events_to_show = events[offset:offset + limit]
    if not events_to_show:
        return ["Больше нет событий для показа"]

    update_at = events_to_show[0]['update_at']
    base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    base_text += f"📅 <b>Завтра:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)}\n\n"

    event_texts = []
    for event in events_to_show:
        event_str = f"• {format_event(event)}\n"
        event_texts.append(event_str)

    # Собираем все тексты событий в один большой текст
    full_text = base_text + "".join(event_texts)

    # Разбиваем на части, если необходимо
    return split_text(full_text, max_length)


def format_events_week(events, offset=0, limit=20, max_length=4096):
    if not events:
        return ["📅 <b>На неделе:</b> нет событий"]

    events_to_show = events[offset:offset + limit]
    if not events_to_show:
        return ["Больше нет событий для показа"]

    update_at = events_to_show[0]['update_at']
    base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    base_text += f"📅 <b>На неделе:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)}\n\n"

    event_texts = []
    for event in events_to_show:
        event_str = f"• {format_event(event)}\n"
        event_texts.append(event_str)

    # Собираем все тексты событий в один большой текст
    full_text = base_text + "".join(event_texts)

    # Разбиваем на части, если необходимо
    return split_text(full_text, max_length)


def sort_today_events(events, importance, offset=0, limit=20):
    if not events:
        return "📅 <b>На сегодня:</b> нет событий с важностью " +'⭐'* importance
    
    events_to_show = events[offset:offset+limit]
    
    if not events_to_show:
        return "Больше нет событий для показа"
    
    update_at = events_to_show[0]['update_at']
    text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    text += f"📅 <b>Сегодня:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)} событий с важностью {'⭐' * importance}\n\n"
    
    for event in events_to_show:
        text += f"• {format_event(event)}\n"
        
    return text


def sort_tomorrow_events(events, importance, offset=0, limit=20):
    if not events:
        return "📅 <b>На завтра:</b> нет событий с важностью "+'⭐' * importance
    
    events_to_show = events[offset:offset+limit]
    
    if not events_to_show:
        return "Больше нет событий для показа"
    
    update_at = events_to_show[0]['update_at']
    text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    text += f"📅 <b>Завтра:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)} событий с важностью {'⭐' * importance}\n\n"
    
    for event in events_to_show:
        text += f"• {format_event(event)}\n"
        
    return text


def sort_week_events(events, importance, offset=0, limit=20):
    if not events:
        return "📅 <b>На неделе:</b> нет событий с важностью " +'⭐'* importance
    
    events_to_show = events[offset:offset+limit]
    
    if not events_to_show:
        return "Больше нет событий для показа"
    
    update_at = events_to_show[0]['update_at']
    text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    text += f"📅 <b>На неделе:</b> показано {offset+1}-{offset+len(events_to_show)} из {len(events)} событий с важностью {'⭐' * importance}\n\n"
    
    for event in events_to_show:
        text += f"• {format_event(event)}\n"
        
    return text


def format_crypto_prices(coins_data, offset=0, limit=20):
    try:
        if not coins_data:
            return "Нет данных о криптовалютах"
        
        coins_to_show = coins_data[offset:offset+limit]
        
        if not coins_to_show:
            return "Больше нет монет для показа"
        
        update_at = coins_to_show[0]['update_at']
        text = f"💰 <b>Котировки криптовалют </b> (обновлено {update_at})\n\n"
        text += f"<i>Показано {offset+1}-{offset+len(coins_to_show)} из {len(coins_data)}</i>\n\n"
        
        for num, coin in enumerate(coins_to_show, start=offset+1):
            ticker = coin['ticker']
            name = coin['name']
            price = coin['price']
            market_cup = coin['market_cup']
            price_change_24hm = coin['price_change_24hm']
            
            change_emoji = "📈" if float(price_change_24hm.replace('%', '').replace(',', '.').replace('−', '-')) >= 0 else "📉"
            
            text += f"{num}) {name} ({ticker}): ${price} | {market_cup} | {change_emoji} {price_change_24hm} за 24ч\n"
            
        return text

    except Exception as e:
        print(f"Ошибка в format_crypto_prices: {e}")
        return "Ошибка при форматировании данных о криптовалютах"
    