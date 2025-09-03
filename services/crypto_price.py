import requests

from bs4 import BeautifulSoup as bs 



def parse_top_coins(limit=100):
    top_coins = []

    url = "https://ru.tradingview.com/markets/cryptocurrencies/prices-all/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        print('Ошибка при загрузке страницы')
        return 0
    
    soup = bs(response.text, 'html.parser')

    table_coins = soup.find('tbody')
    rows = table_coins.find_all('tr')
    
    count = 0
    for row in rows:
        top_coins.append({
            'rank_type': 'top_coin',
            'ticker':row.find('a', class_='apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat').text.strip(),
            'name': row.find('sup', class_='apply-common-tooltip tickerDescription-GrtoTeat').text.strip(),
            'market_cup': row.select('td', class_='cell-RLhfr_y4 left-RLhfr_y4')[4].text.strip(),
            'change_price': row.select('td', class_='cell-RLhfr_y4 left-RLhfr_y4')[3].text.strip(),
            'price': row.select('td', class_='cell-RLhfr_y4 left-RLhfr_y4')[2].text.strip()
        })
        
        count += 1
        if count == limit or count == 100:
            break

    return top_coins
    

def parse_top_gainers():
    top_gainers = []

    url = "https://coinmarketcap.com/gainers-losers/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        print('Ошибка при загрузке страницы')
        return 0
    
    soup = bs(response.text, 'html.parser')

    table_coins = soup.find('tbody')
    rows = table_coins.find_all('tr')
 
    for row in rows:
        name = row.find('div', class_='sc-4c05d6ef-0 sc-dff2ad65-0 dlQYLv hubuLp')
        coin_symbol = row.find('div', class_='sc-dff2ad65-2 qKMrr')

        top_gainers.append({
            'rank_type': 'gainer',
            'ticker': coin_symbol.find('p').text.strip(),
            'name': name.find('p').text.strip(),
            'market_cup': row.find_all('td')[4].text,
            'change_price': row.find('span', class_='sc-d5c03ba0-0 ivIsIp').text,
            'price': row.find('span').text
        })
    

    return top_gainers


def parse_top_losers():
    top_losers = []

    url = "https://coinmarketcap.com/gainers-losers/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        print('Ошибка при загрузке страницы')
        return 0
    
    soup = bs(response.text, 'html.parser')

    table_coins = soup.find_all('div', class_='uikit-col-md-8 uikit-col-sm-16')[1]
    rows = table_coins.find_all('tr')

    for row in rows:
        all_td = row.find_all('td')

        index_volume = 4 
        if index_volume < len(all_td):
            volume = all_td[index_volume].text
        
        change_price_html = row.find('span', class_='sc-d5c03ba0-0 dJLZma')
        if change_price_html:
            change_price = change_price_html.text

        name = row.find('div', class_='sc-4c05d6ef-0 sc-dff2ad65-0 dlQYLv hubuLp')
        if name:
            name_coin = name.find('p').text
            coin_symbol = name.find_all('p')[1].text
            
            top_losers.append({
                'rank_type': 'loser',
                'ticker': coin_symbol,
                'name': name_coin.strip(),
                'market_cup': volume.strip(),
                'change_price': change_price.strip(),
                'price': row.find('span').text
            })

    return top_losers

