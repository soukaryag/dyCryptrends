import re
import coin_fetcher
import price_fetcher
import os
import time
import datetime


def run():
    out = open('out1.txt', 'r')
    coins_found = []
    for line in out:
        temp_tweet = []
        line = line.strip().strip(',').split(',')
        for ent in line:
            temp_tweet.append(ent)
        coins_found.append(temp_tweet)

    date_format = re.compile(r"\S\S\S\s\S\S\S\s(\d\d)\s(\d\d):(\d\d):(\d\d)")    #Format: Wed Jan 03 21:38:53 +0000 2018

    start_time = list((re.search(date_format, coins_found[0][-1])).groups())
    final_time = list((re.search(date_format, coins_found[-1][-1])).groups())

    delta_day = 0
    delta_hour = 0
    delta_minute = int(final_time[2]) - int(start_time[2])
    delta_second = int(final_time[3]) - int(start_time[3])

    WAIT_TIME = 3

    for y in range(1, len(coins_found)):
        first_time = list((re.search(date_format, coins_found[(y - 1)][-1])).groups())
        second_time = list((re.search(date_format, coins_found[y][-1])).groups())
        if (int(second_time[2]) - int(first_time[2])) < WAIT_TIME:
            delta_day = delta_day + (int(second_time[0]) - int(first_time[0]))
            delta_hour = delta_hour + (int(second_time[1]) - int(first_time[1]))
            delta_minute = delta_minute + (int(second_time[2]) - int(first_time[2]))
            delta_second = delta_second + (int(second_time[3]) - int(first_time[3]))

    time_elapsed = (delta_day * 24 * 60) + (delta_hour * 60) + delta_minute + (delta_second / 60)

    time_rounded = str(round(time_elapsed, 2))
    print(time_rounded + " Minutes")
    #print(start_time, final_time)

    coins_abb_dollar, coins_dict, coins_abb = coin_fetcher.all_coins()
    MINIMUM_VIEWS_PER_MINUTE = 50                                      #TWEAK the amount of views/min needed to show up
    MINIMUM_HYPE = int(time_elapsed) * MINIMUM_VIEWS_PER_MINUTE
    MINIMUM_NEGATIVE = 2
    MINIMUM_POSITIVE = 0

    month = time.localtime()[1]
    day = time.localtime()[2]
    hour = time.localtime()[3]
    minute = time.localtime()[4]
    if len(str(month)) < 2:
        month = ("0" + str(month))
    if len(str(day)) < 2:
        day = ("0" + str(day))
    if len(str(hour)) < 2:
        hour = ("0" + str(hour))
    if len(str(minute)) < 2:
        minute = ("0" + str(minute))

    filename = str(time.localtime()[0]) + str(month) + str(day) + str(hour) + str(minute) + " RUNTIME " \
               + time_rounded + "min.txt"

    path = os.getcwd() + "\old_data"
    os.chdir(path)

    out = open(filename, 'w')
    out.write("COIN " + (start_time[0] + " " + start_time[1] + ":" + start_time[2] + ":" + start_time[3]) + " -5hrs," +
              "UNKNOWN VIEWS," + "POSITIVE VIEWS," + "NEGATIVE VIEWS," + "UNKNOWN COUNT," + "GOOD COUNT," +
              "BAD COUNT," + "PERCENT UP," + "START BTC PRICE," +
              "START USD PRICE (" + str(datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')) + ")")
    out.write('\n')
    out.close()
    #print(coins_abb)
    for element in coins_abb:
        count_bad = 0
        count_good = 0
        count_un = 0
        outreach_good = 0                                                        #number of followers that saw the tweet
        outreach_bad = 0
        outreach_un = 0
        for itr_list in coins_found:
            for element2 in range(0, len(itr_list)):
                if element == itr_list[element2]:
                    #print(element)
                    try:
                        if itr_list[element2 + 1] == "-1":
                            count_bad = count_bad + 1
                            outreach_bad = outreach_bad + int(itr_list[-2])
                        elif itr_list[element2 + 1] == "1":
                            count_good = count_good + 1
                            outreach_good = outreach_good + int(itr_list[-2])
                        elif itr_list[element2 + 1] == "0":
                            count_un = count_un + 1
                            outreach_un = outreach_un + int(itr_list[-2])
                    except IndexError:
                        print("error")
        if (outreach_bad + outreach_good + outreach_un) > MINIMUM_HYPE and count_bad > MINIMUM_NEGATIVE and \
                count_good > MINIMUM_POSITIVE:
        #print(element)
            btc_price, usd_price, prct = price_fetcher.find_price(element)
            out = open(filename, 'a')
            out.write(str(element) + "," + str(outreach_un) + "," + str(outreach_good) + "," + str(outreach_bad) + "," +
                      str(count_un) + "," + str(count_good) + "," + str(count_bad) + "," + str(prct) + "," +
                      str(btc_price) + "," + str(usd_price))
            out.write('\n')
            out.close()

run()
