from craigslist import *
from craiglistPost import *
from treeCollector import *
from datacollection.util.util import *
from pymongo import MongoClient
from craigslist import *

import os
import os.path
import json
import datetime
import time
import schedule



# modify the base filter for craigslist such that you can now search by
# search distance in all situations.
CraigslistBase.base_filters['search_distance'] = {'url_key': 'search_distance', 'value': None}
CraigslistBase.base_filters['postal'] = {'url_key': 'postal', 'value': None}


'''
    Problems:
        One of the major problems I have is that I don't get results from
        my scrapping till the next day.


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
        =============================================
        fields: the fields not present in the
    '''
    def sample(self, fields=["attrs", "notices", "body", "imageUrls"]):
        query = CraigslistCommunity(site="boston", category="act")
        results = query.get_results(limit=1, geotagged=True)

        for result in results:

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

            return post.data

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
        results = query.get_results(geotagged=geoTagged)


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
        TODO: display this on a map so we see that we are covering the
        whole area of Boston.


        TEST: does it save progress and resume the next day

    '''
    def scrapeByGrid(self, progress, deeper=True):

        # load the list of zip codes
        f = open("data/bostonZipCodes.txt", "r")
        codes = f.read().split("\n")
        f.close()

        lastZip = 0
        if(os.path.exists("data/progress/lastZip.txt")):
            f2 = open("data/progress/lastZip.txt", "r")
            lastZip = int(f2.read())
            f2.close()

        # tree containing all the progress to made in scrapping so
        # far. It's a modification of the all.json searchtree.
        progressTree = progress
        if(os.path.exists("data/progress/trees/all.json")):
            treeFile = open("data/progress/trees/all.json", "r")
            progressTree = treeFile.read()
            treeFile.close()

        print(codes)

        for term in progress:
            for codeIndex in range(0, len(codes)):
                # run a search on that zip codes
                query = run_search(term["parent"], term["searchTerm"], filters={
                    "search_distance" : 36, # this is the max distance from the center of Dorchester,
                                            # the largest city in Boston
                    "postal" : codes[codeIndex]
                })

                results = query.get_results()

                for result in results:

                    data = result # temperary buffer for current result

                    # Checks to see if the record is already present in the db
                    recordPresent = self.db[term["parent"]].find({"id" : data["id"]}).count() > 0

                    # add additional fields
                    if(deeper and not recordPresent):
                        post = CraigslistPost(result)
                        post.retrieveAttrs()
                        post.retrieveNotices()
                        post.retrieveBody()
                        #post.retrieveImageUrls()

                        data = post.data

                    # store the result
                    if(not recordPresent):
                        self.db[term["parent"]].insert_one(data)


                    # if the scrapper is scheduled to stop,
                    # save the last zip code
                    currentTime = datetime.datetime.now()
                    todayAtHour = currentTime.replace(
                        hour=int(self.endTime[:2]),
                        minute=int(self.endTime[3:5]),
                        second=0, microsecond=0
                    )
                    if(currentTime >= todayAtHour):
                        f2 = open("data/progress/lastZip.txt", "w")
                        f2.write(codes[codeIndex])
                        f2.close()








    '''
        Scrappes the results that have not been scraped
        yet from today.

    '''
    def collectConcentricCircles(self, progress):


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
        pause: the amount of time to wait between scrapes
        resCount: the amount of results to scrape before pausing
        deeper: whether to scrape the actual postings as well
    '''
    def collectToday(self, termList, start, pause, resCount, deeper=True):
        rec = open("data/progress/record.txt", "a")
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
                        todayAtHour = currentTime.replace(
                            hour=int(self.endTime[:2]),
                            minute=int(self.endTime[3:5]),
                            second=0, microsecond=0
                        )
                        if(currentTime >= todayAtHour):
                            print("Paused scrapping for the day.")
                            print("Scrapping will resume again at " + self.endTime)
                            rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")

                            # save progress
                            prog = open("progress.txt", "w")
                            #prog.write(str(index))
                            prog.write(str(resNum))
                            prog.close()

        rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")




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


        last = open("data/progress/lastRecord.txt", "w") # information about the last record scrapped
        rec = open("data/progress/record.txt", "a")
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
                    last.write(data["id"])

                    # Checks to see if the record is already present in the db
                    recordPresent = self.db[term["parent"]].find({"id" : data["id"]}).count() > 0

                    # add additional fields
                    if(deeper and not recordPresent):
                        post = CraigslistPost(result)
                        post.retrieveAttrs()
                        post.retrieveNotices()
                        post.retrieveBody()
                        #post.retrieveImageUrls()

                        data = post.data

                    # store the result
                    #print(result)
                    if(not recordPresent):
                        self.db[term["parent"]].insert_one(data)

                    resNum += 1


                    curCount += 1
                    if(curCount % resCount == 0):
                        time.sleep(waitTime)

                        # check the time.
                        # if the time is 9am stop scrapping,
                        # otherwise continue
                        currentTime = datetime.datetime.now()
                        todayAtHour = currentTime.replace(
                            hour=int(self.endTime[:2]),
                            minute=int(self.endTime[3:5]),
                            second=0, microsecond=0
                        )
                        if(currentTime >= todayAtHour):
                            print("Paused scrapping for the day.")
                            print("Scrapping will resume at 5pm tonight.")
                            rec.write("paused scrapping" + str(datetime.datetime.now()) + "\n")

                            # save progress
                            prog = open("data/progress/progress.txt", "w")
                            #prog.write(str(index))
                            prog.write(str(resNum))
                            prog.close()

        rec.write("ended scrapping" + str(datetime.datetime.now()) + "\n")
        rec.close()
        last.close()


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
        f = open("data/searchTrees/all.json", "r")
        craigslistTree = json.loads(f.read())
        craigslistList = self.buildList(craigslistTree)
        f.close()

        # load progress
        index = 0
        if(os.path.isfile("data/searchTrees/progress.txt")):
            f2 = open("data/searchTrees/progress.txt", "r")
            index = int(f2.read())
            f2.close()

        # Scrapes data from craiglist
        # params: termList, start, waitTime, resCount, deeper=True
        #self.scrapeToday(craiglistList, index, 0, 20)
        self.scrapeByGrid(craigslistList)


    '''
        Schedules a scrapping activity
        ========================================
        startTime: time of day to start scrapping
        endTime: hour of day to end scrapping
    '''
    def scheduleScrape(self, startTime, endTime):
        self.endTime = endTime
        schedule.every().day.at(startTime).do(self.scrapeJob)
        while True:
            schedule.run_pending()
            time.sleep(1)
