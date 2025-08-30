from datetime import datetime



def format_event(event):
    if 'event_date' in event:
        date = event['event_date']
    else:
        date = ''

    time = event['event_time']
    currency = event['currency']
    stars = '★' * event['importance']
    event_name = event['event_name']
    forecast = event['forecast']
    prev = event['prev']
   
    return (
        f'''⏰ <b>{time}</b> {date}
   🏦Валюта: {currency}
   ⭐Важность: {stars}
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


def format_events_today(today_events, max_length=4096):
    if today_events:
        update_at = today_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"
    
    if today_events and today_events[0]:
        text =  f"📅 <b>Сегодня:</b> {len(today_events)} событий\n\n"
        
        parts = []
        
        for event in today_events:
            event_text = f"• {format_event(event)}\n"
            
            if len(text + event_text) > max_length:
                parts.append(text)
                text = base_text + f"📅 <b>Сегодня (продолжение):</b>\n\n{event_text}"
            else:
                text += event_text

        parts.append(text)
        
        return parts
    else:
        return [base_text + "📅 <b>На сегодня:</b> нет событий"]


def format_events_tomorrow(tomorrow_events, max_length=4096):
    if tomorrow_events:
        update_at = tomorrow_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"

    if tomorrow_events and tomorrow_events[0]:
        text = base_text + f"📅 <b>Завтра:</b> {len(tomorrow_events)} событий\n\n"
        
        parts = []
        
        for event in tomorrow_events:
            event_text = f"• {format_event(event)}\n"
            
            if len(text + event_text) > max_length:
                parts.append(text)
                text = base_text + f"📅 <b>Завтра (продолжение):</b>\n\n{event_text}"
            else:
                text += event_text

        parts.append(text)
        
        return parts
    else:
        return [base_text + "📅 <b>На завтра:</b> нет событий"]


def format_events_week(week_events, max_length=4096):
    if week_events:
        update_at = week_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"

    if week_events and week_events[0]:
        text = base_text + f"📅 <b>На неделю:</b> {len(week_events)} событий\n\n"
        
        parts = []
        
        for event in week_events:
            event_text = f"• {format_event(event)}\n"
            
            if len(text + event_text) > max_length:
                parts.append(text)
                text = base_text + f"📅 <b>На неделю (продолжение):</b>\n\n{event_text}"
            else:
                text += event_text

        parts.append(text)
        
        return parts
    else:
        return [base_text + "📅 <b>На неделю:</b> нет событий"]
    

def sort_tomorrow_events(tomorrow_events, stars):
    if tomorrow_events:
        update_at = tomorrow_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"

    if tomorrow_events and tomorrow_events[0]:
        tomorrow_events_by_stars = [event for event in tomorrow_events if event['importance'] == stars]

        base_text += f"📅 <b>:</b> {len(tomorrow_events_by_stars)} {'⭐' * stars} событий\n"

        for event in tomorrow_events_by_stars:
            base_text += f"• {format_event(event)}\n"
        base_text += "\n"

    else:
        base_text += f"📅 <b>На завтра:</b> нет {'⭐' * stars} событий\n\n"

    return base_text


def sort_today_events(today_events, stars):
    if today_events:
        update_at = today_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"

    if today_events and today_events[0]:
        today_events_by_stars = [event for event in today_events if event['importance'] == stars]

        base_text += f"📅 <b>:</b> {len(today_events_by_stars)} {'⭐' * stars} событий\n"

        for event in today_events_by_stars:
            base_text += f"• {format_event(event)}\n"
        base_text += "\n"

    else:
        base_text += f"📅 <b>На сегодня:</b> нет {'⭐' * stars} событий\n\n"

    return base_text


def sort_week_events(week_events, stars):
    if week_events:
        update_at = week_events[0]['update_at']

        base_text = f"📊 <b>Экономический календарь</b> (обновлено {update_at})\n\n"
    else:
        base_text = f"📊 <b>Экономический календарь</b>\n\n"

    if week_events and week_events[0]:
        week_events_by_stars = [event for event in week_events if event['importance'] == stars]

        base_text += f"📅 <b>:</b> {len(week_events_by_stars)} {'⭐' * stars} событий\n"

        for event in week_events_by_stars:
            base_text += f"• {format_event(event)}\n"
        base_text += "\n"

    else:
        base_text += f"📅 <b>На сегодня:</b> нет {'⭐' * stars} событий\n\n"

    return base_text


def format_crypto_prices(price_data, period = '24h'):
    text = "💰 <b>Котировки криптовалют</b>\n\n"
    
    for coin in price_data:
        price = price_data[coin].get('usd')
        change = price_data[coin].get(f'usd_{period}_change', 0)
        arrow = "📈" if change >= 0 else "📉"
        text += f"{coin}: ${price} | {arrow} {change:+.2f}% за {period}\n"
    return text
