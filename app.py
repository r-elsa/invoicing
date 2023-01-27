from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content

@app.route("/page/<int:id>")
def page3(id):
    return "Tämä on sivu " + str(id)

