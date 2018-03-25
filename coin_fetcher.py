import urllib.request
import re


def all_coins():
    market_url = "https://coinmarketcap.com/all/views/all/"
    stream = urllib.request.urlopen(market_url)

    coin_search = re.compile(r'currencies/([\w\d]+-?[\w\d]*)/">(\w+)</a></span>')

    coin_list = []
    coin_list_temp = []
    coin_name = {}
    for line in stream:
        line = str(line.decode("utf-8").strip().split())
        #print(line)
        coin_find = re.search(coin_search, line)
        if coin_find:
            coin_list_temp.append(coin_find[2])
            coin_name[coin_find[2]] = coin_find[1]

    HOW_MANY_COINS = 300                                    #TWEAK to get the top x number of coins analyzed
    coin_list2 = []

    for element in range(0, HOW_MANY_COINS):
        coin_list2.append(coin_list_temp[element])

    for item in coin_list2:
        coin_list.append("$" + item)

    return coin_list, coin_name, coin_list2

#print(all_coins()[1]['ETH'])        #Test Case
