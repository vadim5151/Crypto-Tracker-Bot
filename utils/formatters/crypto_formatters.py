def format_crypto_prices(coins_data, offset=0, limit=20):
    try:
        if not coins_data:
            return "Нет данных о криптовалютах"
        
        coins_to_show = coins_data[offset:offset+limit]
        
        if not coins_to_show:
            return "Больше нет монет для показа"
        
        update_at = coins_to_show[0]['update_at']
        text = f"💰 <b>Котировки криптовалют </b> (обновлено {update_at})\n\n"
        text += f"<b><i>Показано {offset+1}-{offset+len(coins_to_show)} из {len(coins_data)}</i></b>\n\n"
        
        for num, coin in enumerate(coins_to_show, start=offset+1):
            ticker = coin['ticker']
            name = coin['name']
            price = coin['price']
            market_cup = coin['market_cup']
            price_change_24hm = coin['price_change_24hm']
            
            change_emoji = "📈" if float(price_change_24hm.replace('%', '').replace(',', '.').replace('−', '-')) >= 0 else "📉"
            
            text += f"<b>{num}) {name} ({ticker}): ${price} | {market_cup} | {change_emoji} {price_change_24hm} за 24ч</b>\n\n"
            
        return text

    except Exception as e:
        print(f"Ошибка в format_crypto_prices: {e}")
        return "Ошибка при форматировании данных о криптовалютах"