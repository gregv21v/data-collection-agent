'''
    A data source is process
    commands and operates on data
'''

from datacollection.dataSources.dataSource import *
from datacollection.collectors.meetupCollector import *

class MeetupDataSource(DataSource):

    def __init__(self):
        self.name = "meetup"
        #self.collector = MeetupCollector()


    # Decides what to do with the
    # command.
    def processCmd(self):
        # do stuff with craigslist
        cmd = Command("")
        while(cmd.name != "exit"):
            cmd = Command(raw_input(">>"))



    # Displays the help menu.
    def help(self):
        pass
