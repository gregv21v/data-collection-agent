'''
    Here is the timing routine
    that will be used for scrapping
    craigslist in the future.

    Stages:
        Develop timing mechanism.
        (DONE) Create a fictious scenario to better understand how the tree
            is going to integrate in to the timing scheme.
        (DONE) Add access to craigslist without actually scrapping
            Basically, searches are made, but no data is taken
            from those searches. I will leave this timing
            scheme running overnight, which means I have to
            implement something that will run even when I am
            not accessing the terminal of the server. (I can ask
            Tony about this.)
        (DONE) Add access to craigslist with scrapping
            The data from craigslist will actually be collected,
            but none of it will actually be stored. Once this
            stage is successful, I will begin to store the results.

            1. Collect only the basic data. Don't dig into the links
            yet. That can be done later.
            2. Now dig into the links.

        (DONE) Start the scrapping at 10pm, then end at 9am.
            Those hours are the peak scrapping times,
            because craigslist has the least traffic at
            those times.

        (DONE) Add access to craigslist with storing
            Now we can store the data because we know it works.

        Store the data with the extra link information
'''

import time
import json
import schedule
import pprint
from util import *

pp = pprint.PrettyPrinter(indent=4)

'''
    Restructure the search tree into
    a list so that it is easier to
    work with.

    Each entry will end up like this:
        {category, subcategory, name, term}
'''
def buildList(tree, depth=0):
    res = []

    for child in tree["children"]:
        if("children" in child): # child has children
            newChild = child
            if(depth == 1):
                newChild = merge_dicts(child, {"parent" : tree["name"]})
            elif(depth > 1):
                newChild = merge_dicts(child, {"parent" : tree["parent"]})
            res += buildList(newChild, depth+1)
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
    A useful function for printing the
    child.
'''
def printChild(child):
    print(str(child))


'''
    A useful function for printing the
    parent.
'''
def printParent(parent):
    # remove children fields
    newParent = {}
    for key in parent:
        if(key != "children"):
            newParent[key] = parent[key]
    print(newParent)

'''
    Process each child
    individually.
'''
def processChild(tree, parentFunc, childFunc):
    for child in tree["children"]:
        if("children" in child): # child has children
            parentFunc(child)
            processChild(child, parentFunc, childFunc)
        else:
            childFunc(child)

'''
    Scrapes craigslist data from a defined starting
    location.

    <============================================>
    termList: the search terms
    start: the starting index of the search terms
    waitTime: time to wait in between scrapes
    resCount: the number of results that are scrapped
        before waiting.
'''
def scrape(termList, start, waitTime, resCount):
    rec = open("record.txt", "a")
    rec.write("started scrapping" + datetime.datetime.now())

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
            for result in results:

                # store the result
                self.db[term["parent"]].insert_one(result)


                resNum += 1


                curCount += 1
                if(curCount % resCount == 0):
                    time.sleep(waitTime)

                    # check the time.
                    # if the time is 9am stop scrapping,
                    # otherwise continue
                    currentTime = datetime.datetime.now()
                    if(currentTime.hour >= 9):
                        #print("Stopped time")
                        rec.write("ended scrapping" + datetime.datetime.now())

                        # save progress
                        prog = open("progress.txt", "w")
                        prog.write(index)
                        prog.write(resNum)
                        prog.close()

    rec.write("ended scrapping" + datetime.datetime.now())


'''
    The scheduled job for scrapping craigslist
'''
def scrapeJob():
    print("Scrapping Data")

    # load search tree
    f = open("modifiedTrees/all.json", "r")
    craigslistTree = json.loads(f.read())
    craigslistList = buildList(craigslistTree)
    f.close()

    # load progress
    f2 = open("progress.txt", "r")
    index = int(f2.read())
    f2.close()

    scrape(craigslistList, index, 60, 100)




schedule.every().day.at("22:00").do(scrapeData)

while True:
    schedule.run_pending()
    time.sleep(1)
