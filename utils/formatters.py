from datetime import datetime



def format_event(event):
    time = event['time']
    currency = event['currency']
    stars = '★' * event['stars']
    event_name = event['event']
    forecast = event['forecast']
    prev = event['prev']
   
    return (
        f'''⏰ <b>{time}</b>
   🏦Валюта: {currency}
   ⭐Важность: {stars}
   📊 Событие: {event_name}
   📈 Прогноз: {forecast} | Пред.: {prev}
        '''
    )
    

def format_daily(today_events, tomorrow_events):
    current_time = datetime.now().strftime("%H:%M")
    
    text = f"📊 <b>Экономический календарь</b> (обновлено {current_time})\n\n"
    
    if today_events[0] != 'Событий не запланировано':
        text += f"📅 <b>Сегодня:</b> {len(today_events)} событий\n"

        important_today = [event for event in today_events if event['stars'] >= 2][:3]

        for event in important_today:
            text += f"• {format_event(event)}\n"
        text += "\n"

    else:
        text += "📅 <b>Сегодня:</b> нет событий\n\n"
    
    if tomorrow_events[0] != 'Событий не запланировано':
        text += f"📅 <b>Завтра:</b> {len(tomorrow_events)} событий\n"

        important_tomorrow =[event for event in tomorrow_events if event['stars'] >= 2][:3]

        for event in important_tomorrow:
            text += f"• {format_event(event)}\n"
    else:
        text += "📅 <b>Завтра:</b> нет событий"
    
    return text+'...\n Посмотреть больше событий'


def format_events_today(today_events, max_length=4096):
    current_time = datetime.now().strftime("%H:%M")

    base_text = f"📊 <b>Экономический календарь</b> (обновлено {current_time})\n\n"
    
    if today_events and today_events[0] != 'Событий не запланировано':
        text = base_text + f"📅 <b>Сегодня:</b> {len(today_events)} событий\n\n"
        
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
        return [base_text + "📅 <b>Сегодня:</b> нет событий"]


def format_events_tomorrow(tomorrow_events, max_length=4096):
    current_time = datetime.now().strftime("%H:%M")

    base_text = f"📊 <b>Экономический календарь</b> (обновлено {current_time})\n\n"
    
    if tomorrow_events and tomorrow_events[0] != 'Событий не запланировано':
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
        return [base_text + "📅 <b>Завтра:</b> нет событий"]


def format_crypto_prices(price_data, period = '24h'):
    text = "💰 <b>Котировки криптовалют</b>\n\n"
    
    for coin in price_data:
        price = price_data[coin].get('usd')
        change = price_data[coin].get(f'usd_{period}_change', 0)
        arrow = "📈" if change >= 0 else "📉"
        text += f"{coin}: ${price} | {arrow} {change:+.2f}% за {period}\n"
    return text
