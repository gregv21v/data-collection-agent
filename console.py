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

# TODO: Schedule data collection



print("Which source do you want to scrape from?")
print("Type 'options' or 'o' to see what sources are available.")

choice = raw_input(">")

if(choice == "options" or choice == "o"):
    print("Craigslist (c)")
    print("Yelp (y)")
    print("Meetup (m)")
elif(choice == "craigslist" or choice == "c"):
    #print("Craigslist ==> ")
    dataSource = CraigslistDataSource()
    dataSource.processCmd()
elif(choice == "yelp" or choice == "y"):
    #print("Yelp: ")
    dataSource = YelpDataSource()
    dataSource.processCmd()
elif(choice == "meetup" or choice == "m"):
    #print("Meetup: ")
    dataSource = MeetupDataSource()
    dataSource.processCmd()








#choice =
