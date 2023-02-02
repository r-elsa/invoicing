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


#Models
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


class Users(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    

    def __init__(self, username,email,password ):
        self.username=username
        self.email= email
        self.password=password







# Backend


@app.route("/")
def index():
    db.create_all()
    return render_template("login.html")

    """ result = db.session.execute(text(f"SELECT content FROM invoicess"))
    messages = result.fetchall()
    return render_template("mall_index.html", count=len(messages), messages=messages)   """



@app.route("/dashboard", methods=["POST"])
def dashboard():
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    #tietokantakysely -- users if username exists ---> RENDER all invoices of user
    # if user not exists ----> create user 
    #dashboard.html render alla invoices

    return render_template("dashboard.html", username=username, password=password)




@app.route("/new", methods=["POST"])
def create_new_invoice():
    return render_template("createinvoice.html")


@app.route("/", methods=["POST"])
def new_invoice():
    #invoice_number = request.form["invoice"]
    service = request.form["service"]

    taxpercentage = request.form.getlist("taxpercentage")
    message = request.form["message"]
    # store values in database.

    #sql = "INSERT INTO invoices (content) VALUES (:content)"
    #db.session.execute(sql, {"content":content})
    #db.session.commit()
   
    return render_template("invoice.html", service = service,
                                            taxpercentage = taxpercentage,
                                            message=message
    )



@app.route("/dashboard/invoice/<int:id>")
def page3(id):
    return "This is invoice number " + str(id)




#################################################################
@app.route("/mall_new")
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





