from apscheduler.schedulers.blocking import BlockingScheduler
import append_data
import datetime
import os


def some_job():
    append_data.run()
    print("Run at: " + datetime.datetime.now().strftime('%b-%d-%I%M%p-%G'))
    os.chdir("C:/Users/souka/PycharmProjects/CryptoShilling")

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()
