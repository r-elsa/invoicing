from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
#from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Models


class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    

    def __init__(self, username,email,password ):
        self.username=username
        self.email= email
        self.password=password


class Client(db.Model):
    __tablename__= "client"
    id = db.Column(db.Integer, primary_key =True)  ## client has many invoices
    name = db.Column(db.String(200))

    def __init__(self, name ):
        self.name= name
 


class Project(db.Model):
    __tablename__="project"
    id = db.Column(db.Integer, primary_key =True) ##  project has many invoices, primary key to invoice that belongs to project
    name = db.Column(db.String(200), unique = True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name =name
        self.description = description
      

class Invoice(db.Model):
    __tablename__="invoice"
    id = db.Column(db.Integer, primary_key =True)
    sender = db.Column(db.Integer)  # key to user who sent invoice
    project_id = db.Column(db.Integer, primary_key =True)  ## key to Project
    client_id = db.Column(db.Integer) # connect to client
    summary = db.Column(db.String(200))
    raised_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(200))
    tax_type = db.Column(db.Integer)  # connect to taxtype 
    discount = db.Column(db.Float)
    comment = db.Column(db.String)
    
    
    def __init__(self, sender,project_id, client_id, summary, raised_date, due_date, status, tax_type, discount, comment):
        self.sender=sender
        self.project_id=project_id
        self.client_id=client_id
        self.summary=summary
        self.raised_date=raised_date
        self.due_date=due_date
        self.status=status
        self.tax_type=tax_type
        self.discount=discount
        self.comment=comment



class InvoiceItem(db.Model):
    __tablename__= "invoiceitem"
    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String(200))
    price_per_unit = db.Column(db.Float)
    amount = db.Column(db.Integer)


    def __init__(self, description, price_per_unit, amount):
        self.description = description
        self.price_per_unit= price_per_unit
        self.amount = amount


class TaxType(db.Model):
    __tablename__= "taxtype"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(200))
    percentage = db.Column(db.Float)
    comment = db.Column(db.String(200))

    def __init__(self, name, percentage, comment):
        self.name = name
        self.percentage=percentage
        self.comment= comment

class Payment(db.Model):
    __tablename__= "payment"
    id = db.Column(db.Integer, primary_key =True)
    bank_name = db.Column(db.String(200))
    bank_branch = db.Column(db.String(200))
    invoice_id = db.Column(db.Integer ) # connect to invoice id
    comment = db.Column(db.String(200)) # 
  
  











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





