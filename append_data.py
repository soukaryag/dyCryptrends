import os
import price_fetcher
import datetime


def run():
    def add_to_this(filename):
        os.chdir(r'C:\Users\souka\PycharmProjects\CryptoShilling\old_data')
        file = open(filename, 'r')
        coins = []
        old_file_data = []

        for line in file:
            line = line.strip().split(',')
            old_file_data.append(line)
            coins.append(line[0])
        del coins[0]

        old_file_data[0].append("PERCENT UP,START BTC PRICE,START USD PRICE (" +
                                str(datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')) + ")")

        for coin in range(0, len(coins)):
            btc_price, usd_price, prct = price_fetcher.find_price(coins[coin])
            old_file_data[coin + 1].append(str(prct) + "," + str(btc_price) + "," + str(usd_price))
        clear = open(filename, 'w')
        clear.close()

        for itr_list in old_file_data:
            out = open(filename, 'a')
            for elmnt in itr_list:
                out.write(elmnt + ",")
            out.write('\n')
            out.close()

    path = os.getcwd() + "\old_data"
    os.chdir(path)
    all_files = os.listdir()
    for each in all_files:
        add_to_this(each)

#run()
