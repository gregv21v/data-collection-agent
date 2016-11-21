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
        Add access to craigslist with scrapping
            The data from craigslist will actually be collected,
            but none of it will actually be stored. Once this
            stage is successful, I will begin to store the results.

            1. Collect only the basic data. Don't dig into the links
            yet. That can be done later.
            2. Now dig into the links.

        Add access to craigslist with storing
            Now we can store the data because we know it works.
'''

import time
import json
import pprint
from util import *


bariRoot = "C:\Users\Gregory Venezia\Documents\BARI (Aspire Internship)"
curCount = 0
count = 10 # the amount of results to scrape per cycle
waitTime = 3 # we will likely want the wait time
             # to be variable, because craigslist
             # may be looking for patterns
             # and a consistent wait time would
             # be the easist to detect.


# search tree: for terms to scrape
tree = {
    "name" : "Root",
    "children" : [
        {
            "name" : "activities", # the name of the category
            "count" : 20, # number of results that will result from this query
            "children" : [
                {
                    "name" : "child11", # the name of the category
                    "term" : "c11", # the category name, which is also the search term
                    "count" : 5 # number of results that will result from this query
                },
                {
                    "name" : "child12", # the name of the category
                    "term" : "c12", # the category name, which is also the search term
                    "count" : 20 # number of results that will result from this query
                }
            ]
        },
        {
            "name" : "child1", # the name of the category
            "term" : "c1", # the category name, which is also the search term
            "count" : 15 # number of results that will result from this query
        }
    ]
}

pp = pprint.PrettyPrinter(indent=4)






'''
    reform the search tree into
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

#lst = buildList("tree")



def printChild(child):
    print(str(child))

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


f = open("modifiedTrees/all.json", "r")
craigslistTree = json.loads(f.read())


#processChild(craigslistTree, printParent, printChild)
craigslistList = buildList(craigslistTree)


# first iteration:
# make craigslist searches, but don't scrape any
# results.

#pp.pprint(craigslistList)
for term in craigslistList:
    run_search(term["parent"], term["searchTerm"])

    print("Searched: " + term["parent"] + " " + term["searchTerm"])

    curCount += 1
    if(curCount % 20 == 0):
        print("Waiting some time")












    #time.sleep(waitTime)
