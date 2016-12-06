from flask import Flask
from flask import request

import os
import json
from datacollection.collectors.craigslistCollector import *

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'interface', 'static'),
    static_url_path=''
)

#print(app.static_folder)


@app.route("/")
def hello():
    f = open("interface/index.html", "r")
    page = f.read()
    return page


@app.route("/sample")
def sample():
    print("Getting Samples")
    # Possible collectors
    craigslistCollector = CraigslistCollector()
    #yelpCollector = YelpCollector()
    #meetupCollector = MeetupCollector()

    name = request.args.get('name')

    if(name == "craigslist"):
        return flask.jsonify(craigslistCollector.sample())
    else:
        return json.dumps({})



if __name__ == "__main__":
    app.run()
