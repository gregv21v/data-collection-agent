'''
    This script is designed to answer the following question.

    If you start a query at 11:59pm, and scrape that query up beyond 12am
    are you scrapping the results from the next day now?
        Does craigslist update the query results when you change pages?

'''
from craigslist import *
from datetime import datetime
import schedule
import time


def job():
    print('job running')
    # We are going to use housing because I know it
    # will show a lot for results per day.
    housing = CraigslistHousing(site="boston", filters={
        'posted_today' : True
    })

    results = housing.get_results()
    days = []
    dateChanged = False


    for result in results:
        # get the date of the result 2016-12-02 10:38'
        dateObj = datetime.strptime(result["datetime"], "%Y-%m-%d %H:%M")

        if(not dateObj.day in days):
            days.append(dateObj.day)

        if(len(days) > 1):
            dateChanged = True


    f = open("results.txt", "w")
    f.write(str(dateChanged) + "\n")
    f.write(str(days) + "\n")
    f.close()





# We start off by running a search at 11:56pm
schedule.every().day.at("11:59").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
