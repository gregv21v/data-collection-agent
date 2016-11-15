'''
    A data source is process
    commands and operates on data
'''


from datacollection.collectors.craigslistCollector import *
from shell.dataSources.dataSource import *
from shell.core.command import *

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
            cmd = Command(raw_input("Craigslist>"))
            try:
                if(cmd.name == "collect"):
                    category = cmd.parameters[0]
                    subcategory = cmd.parameters[1]
                    params = cmd.parameters[2]

                    if(category == "all"):
                        print("Scrapping all data (NYI)")
                        # TODO: A timing mechanism is going to need to be
                        # implemented: a way of circumventing craigslist
                        # blocking is required.
                    else:
                        self.collector.collectByCategory(category, subcategory, fields=params)
                elif(cmd.name == "sampleCollect"): # sample shows a quick little example
                    self.collector.sample()
                elif(cmd.name == "sampleStore"):
                    res
                elif(cmd.name == "list"):
                    print("List all the categories and subcategories available.")
                    # GUI NOTE:
                    # This would be nicer to see in a GUI because everything
                    # would be visible all at once. You would be able to see all
                    # the categories, and subcategories at the same time. You
                    # would have a dropdown menu, that would be searchable.
                    # It might be nice to structure this into a "file" tree.
                elif(cmd.name == "help"):
                    self.help()
                else:
                    pass
            except IndexError:
                print("Missing command parameter.")



    '''
        Shows a list of commands
        and how to use them.
    '''
    def help(self):
        print("sample --- displays a sample piece of data")
        print("list --- lists all of the categories and subcategories")
        print("collect [category] [subcategory] [\{additionalFields...\}]--- searches by subcategory")
        print("help --- displays this menu")
