'''
    Here is where we run tests
    on the data collectors.
'''




#from datacollection.collectors.collector import *

from datacollection.collectors.yelpCollector import *
from shell.dataSources.yelpDataSource import *

from datacollection.collectors.craigslistCollector import *
from shell.dataSources.craigslistDataSource import *

#from datacollection.collectors.meetupCollector import *
#from datacollection.dataSources.meetupDataSource import *

from shell.core.command import *

import traceback


print("Which source do you want to scrape from?")
print("Type 'options' or 'o' to see what sources are available.")

exited = False
while(not exited):
    choice = raw_input(">")

    if(choice == "options" or choice == "o"):
        print("Craigslist (c)")
        print("Yelp (y)")
        print("Meetup (m)")
    elif(choice == "craigslist" or choice == "c"):
        #print("Craigslist ==> ")
        try:
            dataSource = CraigslistDataSource()
            dataSource.processCmd()
            exited = True
        except:
            traceback.print_exc("log.lg")
    elif(choice == "yelp" or choice == "y"):
        #print("Yelp: ")
        try:
            dataSource = YelpDataSource()
            dataSource.processCmd()
            exited = True
        except:
            traceback.print_exc("log.lg")
    elif(choice == "meetup" or choice == "m"):
        #print("Meetup: ")
        try:
            dataSource = MeetupDataSource()
            dataSource.processCmd()
            exited = True
        except:
            traceback.print_exc("log.lg")
