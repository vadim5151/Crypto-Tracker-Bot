from datetime import datetime


import aiohttp



async def get_crypto_data(coin: str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_last_updated_at=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
             
            last_updated = data[coin].get('last_updated_at')
            if last_updated:
                data[coin]['last_updated'] = datetime.fromtimestamp(last_updated).strftime('%H:%M:%S')
            
            return data[coin]