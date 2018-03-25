import re
import coin_fetcher
import os


def update():
    out = open('out_count_temp1.txt', 'w')
    out.close()

    out = open('out1.txt', 'r')
    coins_found = []
    for line in out:
        temp_tweet = []
        line = line.strip().strip(',').split(',')
        for coin in line:
            temp_tweet.append(coin)
        coins_found.append(temp_tweet)

    date_format = re.compile(r"\S\S\S\s\S\S\S\s(\d\d)\s(\d\d):(\d\d):(\d\d)")        #Format: Wed Jan 03 21:38:53 +0000 2018

    start_time = list((re.search(date_format, coins_found[0][-1])).groups())
    end_time = list((re.search(date_format, coins_found[-1][-1])).groups())

    delta_day = int(end_time[0]) - int(start_time[0])
    delta_hour = int(end_time[1]) - int(start_time[1])
    delta_minute = int(end_time[2]) - int(start_time[2])
    delta_second = int(end_time[3]) - int(start_time[3])
    time_elapsed = (delta_day*24*60) + (delta_hour*60) + delta_minute + (delta_second/60)

    time_rounded = str(round(time_elapsed, 2))

    coins_abb_dollar, coins_dict, coins_abb = coin_fetcher.all_coins()

    MINIMUM_VIEWS_PER_MINUTE = 1000                                         #TWEAK the amount of views/min needed to show up
    MINIMUM_HYPE = int(time_elapsed) * MINIMUM_VIEWS_PER_MINUTE

    for element in coins_abb:
        count = 0
        outreach = 0                      #number of followers that saw the tweet
        for itr_list in coins_found:
            for element2 in itr_list:
                if element == element2:
                    count = count + 1
                    outreach = outreach + int(itr_list[-2])
        if outreach > MINIMUM_HYPE:
            out = open('out_count_temp.txt', 'a')
            out.write(str(element) + "," + str(outreach))
            out.write('\n')
            out.close()
