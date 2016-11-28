from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    f = open("index.html", "r")
    page = f.read()
    return page

if __name__ == "__main__":
    app.run()
