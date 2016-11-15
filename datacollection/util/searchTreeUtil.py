from util import *
import time
import json
import sys

'''
    Count the number of postings currently on craigslist.
'''
def count_all_posts(searchTree):
    countTable = {"total" : 0} # a table containing the count
                    # of each search query along
                    # with the totals
    for key in searchTree:
        print("Counting " + key + " ...")
        countTable[key] = {"total" : 0}
        for subCategory in searchTree[key]:
            if("categories" in subCategory):
                for subSubCategory in subCategory["categories"]:
                    #print("\t\tSearching " + subSubCategory["searchTerm"] + " ...")

                    query = "http://boston.craigslist.org/search/" + subSubCategory["searchTerm"]
                    count = get_count(query)
                    countTable["total"] += count
                    countTable[key]["total"] += count

                    countTable[key][subSubCategory["searchTerm"]] = count
                    #print("\t" + subSubCategory["searchTerm"] + ": " + str(count))

            else:
                #print("\tSearching " + subCategory["searchTerm"] + " ...")

                query = "http://boston.craigslist.org/search/" + subCategory["searchTerm"]
                count = get_count(query)
                countTable["total"] += count
                countTable[key]["total"] += count

                countTable[key][subCategory["searchTerm"]] = count
                #print("\t" + subCategory["searchTerm"] + ": " + str(count))

        #print(key + ": " + str(subTotal))

    return countTable


'''
    Add the results of a craigslist
    search to a database.

    subCategory is a dictionary:
    {
        "searchTerm" : "term to search for in that subcategory"
        "name" : "Name of subcategory"
    }
'''
def add_search_to_db(category, subCategory, db, filters=None):
    query = run_search(category, subCategory, filters)
    results = query.get_results(geotagged=True)

    # put results in database
    for result in results:
        expandedEntry = expand_entry(result)
        expandedEntry["category"] = subCategory
        db[category].insert_one(expandedEntry)


'''
    Add all the search results from the
    searches made from a tree of categories
    and subcategories.

    Filters must be applicable to all search
    terms in the search tree.
'''
def add_tree_to_database(searchTree, db, filters):
    for key in searchTree:
        for subCategory in searchTree[key]:
            if("categories" in subCategory):
                for subSubCategory in subCategory["categories"]:
                    #print("\t\tSearching " + subSubCategory["searchTerm"] + " ...")

                    add_search_to_db(key, subSubCategory["searchTerm"], db, filters)

            else:
                    #print("\tSearching " + subCategory["searchTerm"] + " ...")

                    add_search_to_db(key, subCategory["searchTerm"], db, filters)

'''
    Add all the search results from the
    searches made from a tree of categories
    and subcategories.

    Filters must be applicable to all search
    terms in the search tree.

    This function is used for debugging purposes.
'''
def add_tree_to_database_debug(searchTree, db, filters):
    startTime = time.time()
    endTime = None
    completed = {}
    f = open("timing.txt", "a")

    try:
        for key in searchTree:
            #junk = raw_input("Press any key to continue...")
            print("Searching " + key + " ...")
            completed[key] = {
                "completed" : False,
                "categories" : []
            }
            for subCategory in searchTree[key]:
                if("categories" in subCategory):
                    completed[key]["categories"].append({
                        "categories" : [],
                        "completed" : False
                    })
                    for subSubCategory in subCategory["categories"]:
                        print("\t\tSearching " + subSubCategory["searchTerm"] + " ...")

                        treeNode = {
                            "name" : subSubCategory["name"],
                            "searchTerm" : subSubCategory["searchTerm"],
                            "completed" : False
                        }

                        add_search_to_db(key, subSubCategory["searchTerm"], db, filters)
                        treeNode["completed"] = True

                        completed[key]["categories"]["categories"].append(treeNode)

                        #print(subSubCategory["searchTerm"] + ":" + str(time.time() - startTime))
                        f.write(subSubCategory["searchTerm"] + ":" + str(time.time() - startTime))

                else:
                        print("\tSearching " + subCategory["searchTerm"] + " ...")

                        newNode = {
                            "name" : subCategory["name"],
                            "searchTerm" : subCategory["searchTerm"],
                            "completed" : False
                        }

                        add_search_to_db(key, subCategory["searchTerm"], db, filters)

                        newNode["completed"] = True
                        completed[key]["categories"].append(newNode)

                        #print(subCategory["searchTerm"] + ":" + str(time.time() - startTime))
                        f.write(subCategory["searchTerm"] + ":" + str(time.time() - startTime))


            completed[key]["completed"] = True
        endTime = time.time()
        print("It took " + str(endTime - startTime) + "s")
        f.close()
    except:
        print("Error: The program stopped unexpectedly.")
        #print("Unexpected error:", sys.exc_info()[0])


        f2 = open("progressTree.json", "w")
        f2.write(json.dumps(completed, indent=4))
        f2.close()

        endTime = time.time()
        print("It took " + str(endTime - startTime) + "s")
        f.close()

        raise



'''
    Resume adding results to the database
    starting where you left off in the
    progress tree.
'''
def resume_tree_addition_to_db_debug(progressTree, db, filters):
    startTime = time.time()
    endTime = None
    completed = {}
    #f = open("timing.txt", "a")
    # load the progress tree


    try:
        for key in progressTree:
            #junk = raw_input("Press any key to continue...")
            print("Searching " + key + " ...")
            completed[key] = {
                "completed" : False,
                "categories" : []
            }
            if(not progressTree[key]["completed"]):
                for subCategory in progressTree[key]["categories"]:
                    #print("Sub Category: " + str(subCategory))
                    if("categories" in subCategory and not subCategory["completed"]):
                        completed[key]["categories"].append({
                            "categories" : [],
                            "completed" : False
                        })

                        for subSubCategory in subCategory["categories"]:
                            if(subSubCategory["completed"]):
                                print("\t\tSearching " + subSubCategory["searchTerm"] + " ...")

                                treeNode = {
                                    "name" : subSubCategory["name"],
                                    "searchTerm" : subSubCategory["searchTerm"],
                                    "completed" : False
                                }

                                add_search_to_db(key, subSubCategory["searchTerm"], db, filters)
                                treeNode["completed"] = True

                                completed[key]["categories"]["categories"].append(treeNode)

                                #print(subSubCategory["searchTerm"] + ":" + str(time.time() - startTime))
                                #f.write(subSubCategory["searchTerm"] + ":" + str(time.time() - startTime))
                    else:
                        #print("Sub Category: " + str(subCategory))
                        if(not subCategory["completed"]):
                            print("\tSearching " + subCategory["searchTerm"] + " ...")

                            newNode = {
                                "name" : subCategory["name"],
                                "searchTerm" : subCategory["searchTerm"],
                                "completed" : False
                            }

                            add_search_to_db(key, subCategory["searchTerm"], db, filters)

                            newNode["completed"] = True
                            completed[key]["categories"].append(newNode)

                            #print(subCategory["searchTerm"] + ":" + str(time.time() - startTime))
                            #f.write(subCategory["searchTerm"] + ":" + str(time.time() - startTime))


            #print(completed)
            completed[key]["completed"] = True
        endTime = time.time()
        print("It took " + str(endTime - startTime) + "s")
        #f.close()
    except:
        print("Error: The program stopped unexpectedly.")
        #print("Unexpected error:", sys.exc_info()[0])


        f2 = open("progressTree2.json", "w")
        f2.write(json.dumps(completed, indent=4))
        f2.close()

        endTime = time.time()
        print("It took " + str(endTime - startTime) + "s")
        #f.close()

        raise
