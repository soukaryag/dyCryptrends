import coin_fetcher
import urllib.request
import re


def find_price(coin_abb):
    coins_abb_dollar, coins_dict, coins_abb = coin_fetcher.all_coins()
    coin_name = coins_dict[coin_abb]
    market_url = "https://coinmarketcap.com/currencies/" + coin_name + "/"
    stream = urllib.request.urlopen(market_url)

    usdprice_search = re.compile(r"'document.title', '=', '\"\S+', '[$](\d+.\d+)', '[(](-?\d+.\d+%)[)]', '\|', 'CoinMarketCap\";'")
    usdprice2_search = re.compile(r"'document.title', '=', '\"\S+', '[(]\S+[)]', '[$](\d+.\d+)', '[(](-?\d+.\d+%)")

    price_amount_btc = 0
    price_amount_usd = 0
    percent_change = 0
    for line in stream:
        line = str(line.decode("utf-8").strip().split())
        #print(line)
        usdprice_find = re.search(usdprice_search, line)
        if usdprice_find:
            price_amount_usd = usdprice_find.groups()[0]
            percent_change = usdprice_find.groups()[1]
        else:
            usdprice2_find = re.search(usdprice2_search, line)
            if usdprice2_find:
                price_amount_usd = usdprice2_find.groups()[0]
                percent_change = usdprice2_find.groups()[1]

    market_url = "https://coinmarketcap.com/currencies/bitcoin/"
    stream = urllib.request.urlopen(market_url)
    btc_usd_price = 1
    for line in stream:
        line = str(line.decode("utf-8").strip().split())
        #print(line)
        usdprice_find = re.search(usdprice_search, line)
        if usdprice_find:
           btc_usd_price = usdprice_find.groups()[0]

    price_amount_btc = str(float(price_amount_usd) / float(btc_usd_price))
    return price_amount_btc, price_amount_usd, percent_change

#print(find_price('BTC'))         #Test Case
