'''
    Collects data that has not been collected
    yet until the specified end time.

    Problems:
        How do you keep track of progress, and how
        much data has been collected thus far?
            I can store the date with the category
            {category, subcategory, name, term, lastResId}

    ==========================================================
    progress ==> contains a list of all the categories, and subcategories
                 with the



    Collect old data by concentric circular regions.
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
