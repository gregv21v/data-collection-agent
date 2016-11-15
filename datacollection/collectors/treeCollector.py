'''
    TreeCollector:
        A tree collector collects
        data based on a tree of search
        terms.

        Tree collectors are nice because
        they save their progress, so if for
        some reason the scrapping process is
        stopped, it can be restarted and resume
        where it left off.

    Example:
        This is used on craigslist because
        the data there is stored in categories,
        and subcategories, and subsubcategories.

        The tree is used instead of linear scrapping
        in craigslist in order to retrieve all the names
        of the categories.
'''
from collector import *
import json

class TreeCollector(Collector):

    def __init__(self):
        self.categoriesTree = {} # shows the search terms made
        self.progressTree = {} # shows the progress made on scrapping


    # load a tree with the progress of a scrape
    def loadProgress(self, path):
        f = open(path, "r")
        self.categoriesTree = json.loads(f.read())
        f.close()

    # load a tree of categories
    def loadCategories(self, path):
        f = open(path, "r")
        self.progressTree = json.loads(f.read())
        f.close()
