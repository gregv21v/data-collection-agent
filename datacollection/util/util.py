
from craigslist import *


# Combines two dictionaries
# together
# http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result



'''
    Runs a craigslist search by specifing
    a category and subcategory.
'''
def run_search(category, subcategory, filters={}):
    #print(category + " , " + subcategory)
    if(category == "community"):
        return CraigslistCommunity(site="boston", category=subcategory, filters=filters)
    elif(category == "housing"):
        return CraigslistHousing(site="boston", category=subcategory, filters=filters)
    elif(category == "jobs"):
        return CraigslistJobs(site="boston", category=subcategory, filters=filters)
    elif(category == "personals"):
        return CraigslistPersonals(site="boston", category=subcategory, filters=filters)
    elif(category == "forSale"):
        return CraigslistForSale(site="boston", category=subcategory, filters=filters)
    elif(category == "events"):
        return CraigslistEvents(site="boston", category=subcategory, filters=filters)
    elif(category == "services"):
        return CraigslistServices(site="boston", category=subcategory, filters=filters)
    elif(category == "gigs"):
        return CraigslistGigs(site="boston", category=subcategory, filters=filters)
    elif(category == "resumes"):
        return CraigslistResumes(site="boston", category=subcategory, filters=filters)
    else:
        return None



'''
    Get the number of results present
    when preforming a search at 'url'.
'''
def get_count(url):
    response = requests_get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return int(soup.select("span.totalcount")[0].contents[0])
