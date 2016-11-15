'''
    A data source is process
    commands and operates on data
'''

from datacollection.dataSources.dataSource import *
from datacollection.collectors.craigslistCollector import *

class CraigslistDataSource(DataSource):

    def __init__(self):
        self.name = "craigslist"
        self.collector = CraigslistCollector()


    '''
        Decides what to do with
        the command.
    '''
    def processCmd(self):
        cmd = Command("")
        while(cmd.name != "exit"):
            cmd = Command(raw_input("Craigslist =>>"))
            if(cmd.name == "collect"):
                searchTerm = cmd.parameters[0]
                print(searchTerm)
                self.collector.collectByCategory("community", "act", fields=["notices"])
            elif(cmd.name == "sample"): # sample shows a quick little example
                self.collector.sample()
            elif(cmd.name == "help"):
                self.help()
            else:
                pass


    '''
        Shows a list of commands
        and information about them.
    '''
    def help(self):
        print("sample --- displays a sample piece of data")
        print("collect [category] [subcategory] --- searches by subcategory")
        print("help --- displays this menu")
