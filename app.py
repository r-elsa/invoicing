from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
'postgresql+psycopg2://elsar'

db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text(f"SELECT content FROM invoices"))
    messages = result.fetchall()
    return render_template("mall_index.html", count=len(messages), messages=messages) 

@app.route("/new")
def new():
    return render_template("mall_new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO invoices (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")


""" from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("login.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form["username"]
    password = request.form["password"]
    return render_template("dashboard.html", username=username, password=password)

@app.route("/dashboard/create", methods=["POST"])
def create():
    invoice_number = request.form["invoice"]
    taxvalue = request.form.getlist("taxvalue")
    message = request.form["message"]
    return render_template("invoice.html", invoice_number = invoice_number,
                                            taxvalue=taxvalue,
                                            message=message
    )



@app.route("/dashboard/invoice/<int:id>")
def page3(id):
    return "This is invoice number " + str(id)




 """