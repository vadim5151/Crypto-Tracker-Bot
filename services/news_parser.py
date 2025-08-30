from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs


class EconomicCalendarParser:
    def __init__(self):
        self.periods = {
            'today': '#timeFrame_today',
            'tomorrow': '#timeFrame_tomorrow',
            'week': '#timeFrame_thisWeek'
        }

    async def run(self):
        all_events = {}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                slow_mo=100
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                await page.goto('https://ru.investing.com/economic-calendar/', timeout=60000)
                
                # Парсим данные для каждого периода
                for period_name, period_selector in self.periods.items():
                    print(f"Парсим данные для периода: {period_name}")
                    
                    # Нажимаем на кнопку периода
                    try:
                        await page.click(period_selector)
                        print(f"Клик на кнопку '{period_name}' выполнен")
                        await page.wait_for_timeout(3000)
                    except Exception as e:
                        print(f"Ошибка при клике на кнопку {period_name}: {e}")
                        continue
                    
                    # Прокручиваем и собираем события
                    await self.scroll_and_collect_events(page)
                    
                    # Парсим события для текущего периода
                    period_events = await self.parse_events(page, period_name)
                    all_events[period_name] = period_events
                    print(f"Собрано событий для {period_name}: {len(period_events)}")
                
                return all_events
                
            except Exception as e:
                print(f"Ошибка при парсинге: {e}")
                return {}
            finally:
                await browser.close()

      
    async def parse_events(self, page, period_name):
        """Парсит события для текущего периода на странице"""
        events_data = []
        
        # Получаем все элементы событий
        event_elements = await page.query_selector_all('.js-event-item')
        
        for element in event_elements:
            try:
                event_html = await element.inner_html()
                event_id = await element.get_attribute('id') or f"event_{len(events_data)}"
                event_datetime = await element.get_attribute('data-event-datetime')
                
                # Парсим HTML события
                soup = bs(event_html, 'html.parser')
                
                # Извлекаем время
                time_element = soup.find('td', class_='first left time js-time')
                time = time_element.text.strip() if time_element else 'N/A'
                
                # Извлекаем валюту
                currency_element = soup.find('td', class_='left flagCur noWrap')
                currency = currency_element.text.strip() if currency_element else 'N/A'
                
                # Извлекаем заголовок
                title_element = soup.find('td', class_="left event")
                title = title_element.get_text(strip=True) if title_element else 'N/A'
                
                # Инициализируем переменные
                actual = 'N/A'
                forecast = 'N/A'
                prev = 'N/A'
                importance_level = 0
                
                # Извлекаем все td элементы
                all_tds = soup.find_all('td')
                
                # Обычно факт, прогноз и предыдущее значение находятся в определенном порядке
                if len(all_tds) >= 7:
                    actual = all_tds[4].text.strip() 
                    forecast = all_tds[5].text.strip() 
                    prev = all_tds[6].text.strip()
                else:
                    # Альтернативный подход: поиск по классам
                    actual_el = soup.find('td', class_='actual')
                    actual = actual_el.text.strip() if actual_el else 'N/A'
                    
                    forecast_el = soup.find('td', class_='forecast')
                    forecast = forecast_el.text.strip() if forecast_el else 'N/A'
                    
                    # Поиск предыдущего значения
                    prev_elements = soup.find_all(class_=lambda x: x and any('previous' in cls.lower() or 'prev' in cls.lower() for cls in x) if x else False)
                    prev = prev_elements[0].text.strip() if prev_elements else 'N/A'

                # Извлекаем важность
                sentiment_element = soup.find('td', class_='left textNum sentiment noWrap')
                if sentiment_element:
                    bull_icons = sentiment_element.find_all('i', class_="grayFullBullishIcon")
                    importance_level = len(bull_icons)
                
                # Добавляем данные события
                events_data.append({
                    'id': event_id,
                    'period': period_name,
                    'date': event_datetime[:10] if event_datetime else 'N/A',
                    'time': time,
                    'currency': currency,
                    'actual': actual,
                    'forecast': forecast,
                    'prev': prev,
                    'importance': importance_level,
                    'title': title
                })
                
            except Exception as e:
                print(f"Ошибка при парсинге события: {e}")
                continue
        
        return events_data
    

    async def scroll_and_collect_events(self, page):
        """Прокручивает страницу и собирает события"""
        last_height = await page.evaluate("() => document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 10
        
        while scroll_attempts < max_attempts:
            # Прокручиваем вниз
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            
            # Ждем подгрузки новых событий
            try:
                await page.wait_for_selector('.js-event-item', timeout=10000)
            except:
                break
            
            # Проверяем, нужно ли продолжать прокрутку
            new_height = await page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height
            
            # Если достигли максимума попыток, выходим
            if scroll_attempts >= 3:
                break


async def fetch_economic_calendar():
    parser = EconomicCalendarParser()
    events = await parser.run()

    if events:
        print(f"Успешно собрано событий: {len(events)}")
    else:
        print("Не удалось собрать события")

    return events

