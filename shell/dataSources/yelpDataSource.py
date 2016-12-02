'''
    A data source is process
    commands and operates on data
'''

# TODO: The data for yelp is going
# to be divided up into regions.

from shell.dataSources.dataSource import *
from datacollection.collectors.yelpCollector import *

class MeetupDataSource(DataSource):

    def __init__(self, name):
        self.name = "yelp"
        self.collector = YelpCollector()


    '''
        Decides what to do with
        the command.
    '''
    def processCmd(self):
        cmd = Command("")
        while(cmd.name != "exit"):
            cmd = Command(raw_input("Craigslist>"))
            try:
                if(cmd.name == "collect"):
                    pass
                elif(cmd.name == "sample"): # sample shows a quick little example
                    self.collector.sample()
                elif(cmd.name == "list"):
                    print("List all the categories and subcategories available.")
                    # This would be nicer to see in a GUI because everything
                    # would be visible all at once. You would be able to see all
                    # the categories, and subcategories at the same time. You
                    # would have a dropdown menu, that would be searchable.
                elif(cmd.name == "help"):
                    self.help()
                else:
                    pass
            except IndexError:
                print("Missing command parameter.")



    # Displays the help menu.
    def help(self):
        print("help          --- shows this menu")
        print("sampleStore   --- store a single piece of data in the default database")
        print("sampleCollect --- collect a single piece of data and display it")
        print("list          --- lists all the categories and subcategories")
        print("exit          --- exits the application")
