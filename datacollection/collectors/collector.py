'''
    The data accumulator is the most basic
    unit of data collection.

    It can both take data from a website,
    and place it in a database.


    All data can be collected as a tree
    of search terms.


    You should be able to answer the question:
        I want this data from this source,
        and I want to do this with it.


    DataCollector ==> Database ==> Graphs ==> Presentation
        \
         \
         Graphs

    What do I want?
        Do I want historic data?
            If so, start saving that data to the the database.


    Interface:
        commands:

    Show sources:
        Yelp
        Craigslist
        Meetup
        ... etc.

'''

import json

class Collector:

    def __init__(self):
        self.name = ""
        self.mongoClient = None
        self.db = None
        pass

    def loadCredentials(self):
        f = open("credentials/" + self.name + "Cred.json", "r")
        cred = json.loads(f.read())
        f.close()

        return cred


    # Collects all the data from the data source
    def collectAll(self):
        print("Collecting...")
        pass

    # Stores data into the mongodb database
    def store(self, data):
        print("Storing...")
        pass

    def sample(self):
        # returns a single result
        print("Example")
        pass
