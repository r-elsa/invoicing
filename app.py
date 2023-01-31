from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

#from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Model
class Invoice(db.Model):
    __tablename__="invoice"
    id = db.Column(db.Integer, primary_key =True)
    sender = db.Column(db.String(200), unique = True)
    message = db.Column(db.String(200))
    price_per_unit = db.Column(db.Integer)
    amount_of_units = db.Column(db.Integer)
    

    def __init__(self, sender, message, price_per_unit, amount_of_units):
        self.sender=sender
        self.message=message
        self.price_per_unit=price_per_unit
        self.amount_of_units=amount_of_units






@app.route("/")
def index():
    db.create_all()
    return 'it works'
    """ result = db.session.execute(text(f"SELECT content FROM invoicess"))
    messages = result.fetchall()
    return render_template("mall_index.html", count=len(messages), messages=messages)   """

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


 
if __name__ == '__main__':
    app.run(debug=True)






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