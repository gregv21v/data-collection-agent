

from craigslist import *
from craiglistPost import *
from treeCollector import *
from datacollection.util.util import *
from pymongo import MongoClient
import json



# TODO: Construct the craigslist class
# TODO: Transfer over the data tree

# NOTE: This is going to take a long time.
# I'm going to have to restructure everything
# that I did, so it likely won't be done today.
# Most of the work is actually pretty streight
# forward it's just very time consuming.

# The project has gotten pretty large,
# so it's going to be more and more difficult
# to understand. I'm going to need to compartmentilize
# things better.





class CraigslistCollector(TreeCollector):


    def __init__(self):
        self.name = "craigslist"
        creds = self.loadCredentials()

        # setup mongo db
        self.mongoClient = MongoClient(
            creds["mongodb"]
        )
        self.db = self.mongoClient.get_default_database()


    '''
        Collects a single entry from the database
    '''
    def sample(self):
        query = CraigslistCommunity(site="boston", category=subCategory)
        results = query.get_results(limit=1)

        for result in results:
            print(result)

    '''
        Collects a single entry from craigslist
        and store it in the database.
    '''
    def sampleStore(self):
        query = CraigslistCommunity(site="boston", category="act")
        results = query.get_results(limit=1)

        for result in results:
            self.db["community"].insert_one(result)



    def collectAll(self):
        pass

    # Store a records in the db.
    def store(self, data):
        for record in records:
            self.mongoClient.insert_one(record)




    # Collect a record by it's id.
    def collectById(self, id):
        pass

    '''
        Collect all the records in a given
        category.
        fields: the fields to include when
        collecting the data. (["attrs", "notices", "body", "imageUrls"])
        Stored determines if the results will be stored as you scrape
    '''
    def collectByCategory(self, category, subCategory, fields=[], geoTagged=True, stored=False):
        print("Collecting by category")
        query = run_search(category, subcategory)
        #run_search(category, subCategory, filters={})
        results = query.get_results(geoTagged=geoTagged)


        #print("Results: " + str(results.__dict__))
        resArray = []

        # Put the results in an array.
        for result in results:
            # append additional fields
            print(result)

            post = CraigslistPost(result)
            for field in fields:
                if(field == "attrs"):
                    post.retrieveAttrs()
                elif(field == "notices"):
                    post.retrieveNotices()
                elif(field == "body"):
                    post.retrieveBody()
                elif(field == "imageUrls"):
                    post.retieveImageUrls()

            if(stored):
                self.db[category].insertOne(post.data)


            resArray.append(result)

        return resArray

    def collectTree(self):
        # go through the search to collect all the data

        # start where the progress tree left off.

        pass
