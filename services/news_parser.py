import aiohttp
from datetime import timedelta, datetime 

from bs4 import BeautifulSoup as bs
import pytz



class EconomicCalendarParser:
    def __init__(self, soup):
        self.soup = soup
        self.current_date = datetime.now(pytz.UTC)


    def extract_events_with_dates(self):
        events = []

        event_rows = self.soup.find_all('tr', class_='js-event-item')

        for row in event_rows:
            event_datetime_str = row.get('data-event-datetime')
            
            event_datetime = datetime.strptime(event_datetime_str, "%Y/%m/%d %H:%M:%S")
            event_datetime = pytz.UTC.localize(event_datetime)

            if event_datetime.date() == self.current_date.date():
                day_type = 'today'
            elif event_datetime.date() == (self.current_date + timedelta(days=1)).date():
                day_type = 'tomorrow'
            
            sentiment = row.find('td', class_="left textNum sentiment noWrap")
            
            events.append({
                'day_type':day_type,
                'time':row.find('td', class_="first left time js-time").text.strip() if row else 'N/A',
                'currency': row.find('td', class_="left flagCur noWrap").text.strip() if row else 'N/A',
                'stars': len(sentiment.find_all('i', class_='grayFullBullishIcon')) if sentiment else 0,
                'event': row.find('td', class_='left event').text.strip() if row else 'N/A',
                'forecast': row.find('td', class_="fore").text.strip() if row else 'N/A',
                'prev': row.find(class_='prev').text.strip() if row else 'N/A'
                
            })
         
        return events
    

    def get_today_events(self):
        events = self.extract_events_with_dates()
        return [event if event['day_type'] == 'today' else 'Событий не запланировано' for event in events ]


    def get_tomorrow_events(self):
        events = self.extract_events_with_dates()
        return [event if event['day_type'] == 'tomorrow' else 'Событий не запланировано' for event in events ]
        


async def fetch_economic_calendar():
    url = 'https://ru.investing.com/economic-calendar/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                html = await response.text()
                
                soup = bs(html, 'html.parser')
                parser = EconomicCalendarParser(soup)
                
                today_events = parser.get_today_events()
                tomorrow_events = parser.get_tomorrow_events()
            
                
                return today_events, tomorrow_events
                
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return [], []
    

