from flask import Flask
from flask import request
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    f = open("index.html", "r")
    page = f.read()
    return page


@app.route("/sample")
def sample():
    dataSource = request.args.get('name')



if __name__ == "__main__":
    app.run()
