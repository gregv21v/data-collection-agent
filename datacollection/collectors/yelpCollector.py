from collector import *
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from pymongo import MongoClient

from bs4 import BeautifulSoup
import json
import requests


# TODO: Add comments describing each function
# TODO: Reorganize functions such that they are smaller and
#       give more options.


class YelpCollector(Collector):


    def __init__(self):
        self.name = "yelp"
        creds = self.loadCredentials()

        # Authenticate Yelp
        auth = Oauth1Authenticator(
            consumer_key=creds["consumer_key"],
            consumer_secret=creds["consumer_secret"],
            token=creds["token"],
            token_secret=creds["token_secret"]
        )
        self.yelpClient = Client(auth)
        self.mongoClient = MongoClient(
            creds["mongodb"]
        )


    '''
        Returns a single result.
    '''
    def sample(self):
        return self.yelpClient.search("Boston, MA", {"limit" : 1})

    def collectBatch(self, offset):
        return self.yelpClient.search(
            "Boston, MA",
            { "offset" : offset }
        )





    ## used for the collection of data
    ## from the website.
    def collectAll(self):
        # the total I get from the api doesn't
        # seem to accurate, so I'm taking a different
        # approach
        response = requests.get("https://www.yelp.com/search?find_loc=Boston,+MA")
        soup = BeautifulSoup(response.content, 'html.parser')

        total = soup.select("span.pagination-results-window")[0].contents[0].strip()[len("Showing 1-10 of "):]

        print(total)

        # expected result: 78189, give or take a few
        firstBatch = self.collectBatch(0)
        #print(firstBatch.total)


    # get the ids for a some businesses
    def getIds(self):
        # the total I get from the api doesn't
        # seem to accurate, so I'm taking a different
        # approach
        response = requests.get("https://www.yelp.com/search?find_loc=Boston,+MA")
        soup = BeautifulSoup(response.content, 'html.parser')

        total = soup.select("span.pagination-results-window")[0].contents[0].strip()[len("Showing 1-10 of "):]
        total = int(total)


        currOffset = 0
        batchNum = 0
        businessIds = []
        while(currOffset < 1):
            print("Batch " + str(batchNum) + " complete.")
            businesses = self.collectBatch(currOffset).businesses
            for business in businesses:
                businessIds.append(business.id)

            currOffset += 20
            batchNum += 1

        return businessIds


    def store(self):
        pass


    def getBusiness(self, id):
        return self.yelpClient.get_business(id)


    # exclude is the bu
    #def collectAndStoreBiz(self, exclude):


    # exclude is the business fields to exclude
    def collectAndStore(self, exclude=[
        "url",
        "mobile_url",
        "rating_img_url",
        "rating_img_url_small",
        "rating_img_url_large",
        "image_url",
        "snippet_image_url",
        "eat24_url",
        "reviews"
    ]):
        db = self.mongoClient.get_default_database()
        # the total I get from the api doesn't
        # seem to accurate, so I'm taking a different
        # approach
        response = requests.get("https://www.yelp.com/search?find_loc=Boston,+MA")
        soup = BeautifulSoup(response.content, 'html.parser')

        total = soup.select("span.pagination-results-window")[0].contents[0].strip()[len("Showing 1-10 of "):]
        total = int(total)
        #print(total)

        # collect the business data
        currOffset = 0
        batchNum = 0
        businessIds = []
        db["info"].insert_one({
            "offset" : 0
        })

        while(currOffset < total):
            print("Batch " + str(batchNum) + " complete.")
            businesses = self.collectBatch(currOffset).businesses
            for business in businesses:
                businessIds.append(business.id)

                #print()
                #JSON = json.dumps(business, default=lambda a: a.)
                #print(business.__dict__)
                dictionary = business.__dict__
                dictionary["location"] = dictionary["location"].__dict__
                dictionary["location"]["coordinate"] = dictionary["location"]["coordinate"].__dict__

                # delete the image urls before adding the object
                # to the database
                for e in exclude:
                    del dictionary[e]

                db["businesses"].insert_one(dictionary)

            currOffset += 20
            # store the offset in the database for future use
            db["info"].update_one({}, {"$inc" : { "offset" : 20 }})

            batchNum += 1



        #print(str(businessIds))
        for bId in businessIds:
            print(bId)

            business = self.yelpClient.get_business(bId).business

            #print(business.__dict__)
            # collect all the reviews data
            ##print("============================================")
            reviews = business.reviews
            if(reviews != None):
                for review in reviews:
                    print(review.__dict__)

            #print(str(business.__dict__))


            # collect all the gift certificate data
            certs = business.gift_certificates
            if(certs != None):
                for cert in certs:
                    #db["gift_certificates"].insert_one()
                    pass


            # collect all the deals data
            deals = business.deals
            if(deals != None):
                for deal in deals:
                    #print(deal.__dict__)
                    pass















    
