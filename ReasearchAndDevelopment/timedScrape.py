'''
    Here is the timing routine
    that will be used for scrapping
    craigslist in the future.

    Stages:
        Develop timing mechanism.
        Create a fictious scenario to better understand how the tree
            is going to integrate in to the timing scheme.
        Add access to craigslist without actually scrapping
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
        Add access to craigslist with storing
            Now we can store the data because we know it works.
'''

import time


bariRoot = "C:\Users\Gregory Venezia\Documents\BARI (Aspire Internship)"
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



'''
    reform the search tree into
    a list so that it is easier to
    work with.
'''
def buildList(tree):
    res = []
    for child in tree["children"]:
        if("children" in child): # child has children
            res += buildList(child)
        else:
            res.append(child)

    return res

#lst = buildList("tree")



def printChild(child):
    print(str(child))

def printParent(parent):
    # remove children fields
    newParent = {
        "name" : parent["name"],
        "count" : parent["count"]
    }
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




#processChild(tree, printParent, printChild)

# 

#while(curCount < maxCount):
    # scrape x results




    #time.sleep(waitTime)
