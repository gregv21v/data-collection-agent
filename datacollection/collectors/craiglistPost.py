
from craigslist import *
from bs4 import BeautifulSoup
import bs4


class CraigslistPost:

    # Data is the original data from
    # the dataset.
    def __init__(self, data):
        self.data = data
        self.soup = None


    # Retrieve the attributes of
    # the post from craigslist.
    def retrieveAttrs(self):
        if(self.soup == None):
            response = requests_get(self.data["url"])
            self.soup = BeautifulSoup(response.content, 'html.parser')

        attrs = []
        attrGroups = self.soup.find_all("p", {"class" : "attrgroup"})

        for attrGroup in attrGroups:
            spans = attrGroup.find_all("span")
            for span in spans:
                #print span
                if len(span.contents) == 1:
                    attrs.append(span.contents)
                else:
                    # strip all the tags from the html
                    # content
                    strippedString = ""

                    # create one string from the entire contents
                    for child in span.children:
                        if isinstance(child, bs4.element.NavigableString):
                            strippedString += child
                        else:
                            strippedString += child.contents[0]

                    attrs.append(strippedString)

        return attrs

    # Retrieve the post body
    # from craigslist
    def retrieveBody(self):
        if(self.soup == None):
            response = requests_get(self.data["url"])
            self.soup = BeautifulSoup(response.content, 'html.parser')

        self.data["body"] = self.soup.select("#postingbody")[0].getText()

        return self.data["body"]

    # get the posting notices
    def retrieveNotices(self):
        if(self.soup == None):
            response = requests_get(self.data["url"])
            self.soup = BeautifulSoup(response.content, 'html.parser')

        noticesHTML = self.soup.select("ul.notices > li")
        notices = []

        for noticeHTML in noticesHTML:
            notices.append(noticeHTML.getText())

        self.data["notices"] = notices

        return notices

    # Gets the image urls from the
    # posting
    def retrieveImageUrls(self):
        if(self.soup == None):
            response = requests_get(self.data["url"])
            self.soup = BeautifulSoup(response.content, 'html.parser')

        thumbNails = self.soup.find_all("a", {"class" : "thumb"})

        if len(thumbNails) == 0:
            # get the image from the img tag.
            imgUrl = self.soup.select("div.slide > img")[0]["src"]

            self.data["images"] = [imgUrl]

            return imgUrl

        else:
            thumbNailUrls = []

            for thumbNail in thumbNails:
                thumbNailUrls.append(thumbNail["href"])

            self.data["images"] = thumbNailUrls

            return thumbNailUrls
