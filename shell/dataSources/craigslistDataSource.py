'''
    A data source is process
    commands and operates on data
'''
from datacollection.collectors.craigslistCollector import *
from dataSource import *
from shell.core.command import *
import schedule
import time
import json

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
                    print(self.collector.sample())
                elif(cmd.name == "sampleStore"):
                    # collects a sample of data and stores it in the database.
                    self.collector.sampleStore()
                elif(cmd.name == "scrapeOld"):
                    # Scrapes old data that has not been scrapped
                    # yet starting from the beginning.
                    f = open("SearchTrees/all.json", "r")
                    tree = json.loads(f.read())

                    lst = self.collector.buildList(tree)
                    self.collector.collectOld(lst)

                elif(cmd.name == "scheduleCollect"):
                    timeOfDay = cmd.parameters[0]
                    schedule.every().day.at(timeOfDay).do(self.collector.scrapeJob)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
                elif(cmd.name == "list"):
                    # load the categories and subcategories file
                    f = open("SearchTrees/all.json", "r")
                    tree = json.loads(f.read())

                    self.listCategories(tree)
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
        print("help          --- displays this menu")
        print("sampleCollect --- displays a sample piece of data")
        print("sampleStore   --- stores a sample piece of data in the default database")
        print("collectOld    --- collects data that has not been collected yet")
        print("list          --- lists all of the categories and subcategories")
        print("collect [category] [subcategory] [\{additionalFields...\}]")
        print("              --- searches by subcategory")
        print("scheduleCollect [time of day]")
        print("              --- collects data at a specific time of day")
        print("exit          --- exits the application")


    '''
        List all the categories and
        subcategories by search term.
    '''
    def listCategories(self, tree, depth=0):
        for child in tree["children"]:
            newChild = child
            if("children" in child): # child has children
                print((" " * depth) + newChild["name"])
                self.listCategories(newChild, depth+1)
            else:
                print((" " * depth) + newChild["searchTerm"])
