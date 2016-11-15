

import meetup.api


class MeetupCollector(Collector):


    def __init__(self):
        self.client = meetup.api.Client("141e381b247744f196e677163693741")

    def sample(self):
        print(self.client.GetGroup({"urlname" : "Testing-Meetup-API"}))

    def sampleGroup(self):
        pass


    def collectAll(self):
        pass



    def store(self, data):
        pass
