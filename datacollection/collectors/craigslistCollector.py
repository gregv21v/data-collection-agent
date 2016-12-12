from craigslist import *
from craiglistPost import *
from treeCollector import *
from datacollection.util.util import *
from pymongo import MongoClient
import os
import json
import datetime
import time





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

'''
    Problems:
        One of the major problems I have is that I don't get results from
        my scrapping till the next day.

'''
'''
    Questions:
        What is the max and min time it takes to scrape all the days
        results from craigslist?

        If you start a query at 11:59pm, and scrape that query up beyond 12am
        are you scrapping the results from the next day now?
            Does craigslist update the query results when you change pages?


'''





class CraigslistCollector(TreeCollector):

    def __init__(self):
        self.name = "craigslist"
        creds = self.loadCredentials()

        # setup mongo db
        self.mongoClient = MongoClient(
            creds["mongodb"]
        )
        self.db = self.mongoClient.get_default_database()
        #self.db["test"].insert_one({"a": 0})





    '''
        Convert the original search tree into a list.

        Each entry will end up like this:
            {category, subcategory, name, term}
    '''
    def buildList(self, tree, depth=0):
        res = []

        for child in tree["children"]:
            if("children" in child): # child has children
                newChild = child
                if(depth == 1):
                    newChild = merge_dicts(child, {"parent" : tree["name"]})
                elif(depth > 1):
                    newChild = merge_dicts(child, {"parent" : tree["parent"]})
                res += self.buildList(newChild, depth+1)
            else:
                #newChild = merge_dicts(child, {"parent" : tree["name"]})
                newChild = child
                if(depth == 1):
                    newChild = merge_dicts(child, {"parent" : tree["name"]})
                elif(depth > 1):
                    newChild = merge_dicts(child, {"parent" : tree["parent"]})
                res.append(newChild)

        return res


    '''
        Collects a single entry from the database
    '''
    def sample(self):
        query = CraigslistCommunity(site="boston", category="act")
        results = query.get_results(limit=1)

        for result in results:
            return result

    '''
        Collects a single entry from craigslist
        and store it in the database.
    '''
    def sampleStore(self):
        query = CraigslistCommunity(site="boston", category="act")
        results = query.get_results(limit=1)

        for result in results:
            self.db["community"].insert_one(result)

    '''
        Store a record in the database.
    '''
    def store(self, data):
        for record in records:
            self.mongoClient.insert_one(record)

    '''
        Collect a record by id.
    '''
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
                    post.retrieveImageUrls()

            if(stored):
                self.db[category].insert_one(post.data)


            resArray.append(result)

        return resArray




    '''
        Scrappes the results that have not been scraped
        yet from today.

    '''
    def collectOld(self, progress):
        # Divide the region into concentric
        # circles.
        index = 0
        for term in progress:
            query = run_search(term["parent"], term["searchTerm"], filters={
                "search_distance" : 5 + index,
                "postal" : 02110
            })
            results = query.get_results()

            # add each result to the database
            for result in results:
                self.db[term["parent"]].insert_one(result)

                # if time is up save the progress to the database

            raw_input("Press enter to continue ...")
            index += 1


    '''
        Collect todays data
        ============================================
        termList: the list of search terms
        start: where in the termList to start scrapping
        waitTime: the amount of time to wait between scrapes
        resCount: the amount of results to scrape before pausing
        deeper: whether to scrape the actual postings as well
    '''
    def collectToday(self, termList, start, waitTime, resCount, deeper=True):
        rec = open("record.txt", "a")
        rec.write("started scrapping " + str(datetime.datetime.now()) + "\n")

        for index in range(start, len(termList)):
            term = termList[index]

            if("searchTerm" in term):
                print("Searched: " + term["parent"] + " " + term["searchTerm"])

                # ====> Interrupt at this point
                # ====> This interrupt allows the program to
                #       only run at certain times.

                query = run_search(term["parent"], term["searchTerm"], filters={
                    "posted_Today" : True
                })
                results = query.get_results()

                resNum = 0 # the result number
                curCount = 0
                for result in results:

                    data = result # temperary buffer for current result

                    # add additional fields
                    if(deeper):
                        post = CraigslistPost(result)
                        post.retrieveAttrs()
                        post.retrieveNotices()
                        post.retrieveBody()
                        #post.retrieveImageUrls()

                        data = post.data

                    # store the result
                    #print(result)
                    if(not self.db[term["parent"]].find({"id" : data["id"]}).count() > 0):
                        self.db[term["parent"]].insert_one(data)

                    resNum += 1
                    curCount += 1
                    if(curCount % resCount == 0):
                        time.sleep(waitTime)

                        # check the time.
                        # if the time is 9am stop scrapping,
                        # otherwise continue
                        currentTime = datetime.datetime.now()
                        if(currentTime.hour >= 14):
                            print("Paused scrapping for the day.")
                            print("Scrapping will resume again the same time it was started.")
                            rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")

                            # save progress
                            prog = open("progress.txt", "w")
                            #prog.write(str(index))
                            prog.write(str(resNum))
                            prog.close()

        rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")
        pass




    '''
        Collect all data
        ==================================================
        termList: the search terms
        start: the starting index of the search terms
        waitTime: time to wait in between scrapes
        resCount: the number of results that are scrapped
            before waiting.
        deeper: whether to scrape the actual postings as well
    '''
    def collectAll(self, termList, start, waitTime, resCount, deeper=True):
        #print("Started Collection")

        rec = open("record.txt", "a")
        rec.write("started scrapping " + str(datetime.datetime.now()) + "\n")

        for index in range(start, len(termList)):
            term = termList[index]

            if("searchTerm" in term):
                print("Searched: " + term["parent"] + " " + term["searchTerm"])

                # ====> Interrupt at this point
                # ====> This interrupt allows the program to
                #       only run at certain times.

                query = run_search(term["parent"], term["searchTerm"])
                results = query.get_results()

                resNum = 0 # the result number
                curCount = 0
                for result in results:

                    data = result # temperary buffer for current result

                    # add additional fields
                    if(deeper):
                        post = CraigslistPost(result)
                        post.retrieveAttrs()
                        post.retrieveNotices()
                        post.retrieveBody()
                        #post.retrieveImageUrls()

                        data = post.data

                    # store the result
                    #print(result)
                    if(not self.db[term["parent"]].find({"id" : data["id"]}).count() > 0):
                        self.db[term["parent"]].insert_one(data)

                    resNum += 1


                    curCount += 1
                    if(curCount % resCount == 0):
                        time.sleep(waitTime)

                        # check the time.
                        # if the time is 9am stop scrapping,
                        # otherwise continue
                        currentTime = datetime.datetime.now()
                        if(currentTime.hour >= 9):
                            print("Paused scrapping for the day.")
                            print("Scrapping will resume at 5pm tonight.")
                            rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")

                            # save progress
                            prog = open("progress.txt", "w")
                            #prog.write(str(index))
                            prog.write(str(resNum))
                            prog.close()

        rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")





    '''
        Collects all the data

        NOTE: The current issue in scrapping craigslist now is that
        it scrapes duplicates. One way to make sure that these duplicates
        aren't added to the database is to check for them before adding them.

        That doesn't solve the problem of scrapping those duplicates though,
        which is still a problem. Lets say the scrapper scrapes x results night
        1. It will scrape those results and only those results again the next
        night if x is less than the total scrappable results from that particular
        field.

        Solving this problem would be easy if the craigslist api provide pagination
        for it's results. I could implement it, but that wouldn't be idea.
    '''
    def scrapeJob(self):
        print("Scrapping Data")

        # load search tree
        # this is not the path I would expect to work
        # apparently its relative to console.py
        f = open("SearchTrees/all.json", "r")
        craigslistTree = json.loads(f.read())
        craigslistList = self.buildList(craigslistTree)
        f.close()

        # load progress
        index = 0
        if(os.path.isfile("progress.txt")):
            f2 = open("progress.txt", "r")
            index = int(f2.read())
            f2.close()

        # Scrapes data from craiglist
        # params: termList, start, waitTime, resCount, deeper=True
        self.collectAll(craigslistList, index, 0, 20)
