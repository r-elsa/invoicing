from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import re

#from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Models


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    

    def __init__(self, username,email,password ):
        self.username=username
        self.email= email
        self.password=password


class Client(db.Model):
    __tablename__= "clients"
    id = db.Column(db.Integer, primary_key =True)  ## client has many invoices
    name = db.Column(db.String(200))

    def __init__(self, name ):
        self.name= name
 


class Project(db.Model):
    __tablename__="projects"
    id = db.Column(db.Integer, primary_key =True) ##  project has many invoices, primary key to invoice that belongs to project
    name = db.Column(db.String(200), unique = True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name =name
        self.description = description
      

class Invoice(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key =True)
    user = db.Column(db.Integer)  # user
    project_name = db.Column(db.String(200))  ## key to Project -name
    client_name = db.Column(db.String(200)) # connect to client
    summary = db.Column(db.String(200))
    raised_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(200))
    tax_type = db.Column(db.Integer)  # connect to taxtype 
    discount = db.Column(db.Float)
    comment = db.Column(db.String)
    
    
    def __init__(self, user,project_name, client_name, summary, raised_date, due_date, status, tax_type, discount, comment):
        self.user =user
        self.project_name=project_name
        self.client_name=client_name
        self.summary=summary
        self.raised_date=raised_date
        self.due_date=due_date
        self.status=status
        self.tax_type=tax_type
        self.discount=discount
        self.comment=comment



class InvoiceItem(db.Model):
    __tablename__= "invoiceitems"
    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String(200))
    price_per_unit = db.Column(db.Float)
    amount = db.Column(db.Integer)


    def __init__(self, description, price_per_unit, amount):
        self.description = description
        self.price_per_unit= price_per_unit
        self.amount = amount


class TaxType(db.Model):
    __tablename__= "taxtypes"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(200))
    percentage = db.Column(db.Float)
    comment = db.Column(db.String(200))

    def __init__(self, name, percentage, comment):
        self.name = name
        self.percentage=percentage
        self.comment= comment

class Payment(db.Model):
    __tablename__= "payments"
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

@app.route("/signup",  methods=["POST", "GET"])
def signup():
    return render_template("signup.html")

    """ result = db.session.execute(text(f"SELECT content FROM invoicess"))
    messages = result.fetchall()
    return render_template("mall_index.html", count=len(messages), messages=messages)   """



@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form["username"]
    password = request.form["password"]
    returntemplate = render_template("dashboard.html", username=username, password=password)
    referralroute = request.referrer

    # sign up
    if referralroute[-6:]=="signup":
        #is username alredy taken
        sql = "SELECT id, username FROM users WHERE username LIKE :username"
        result = db.session.execute(text(sql), {"username":"%"+username+"%"})
        soughtuser = result.fetchall()
        if (len(soughtuser)) > 0:
            returntemplate = render_template("signup.html", errormessage = "Username already taken")
        else:     
            email = request.form["email"]
            sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
            db.session.execute(text(sql), {"username":username, "email":email,"password":password})
            db.session.commit()
    
    #login
    
    else:
        sql = "SELECT id, email FROM users WHERE username LIKE :username AND password LIKE :password"
        result = db.session.execute(text(sql), {"username":"%"+username+"%", "password":"%"+password+"%"})
        soughtuser = result.fetchall()
        if (len(soughtuser)) == 0:
            returntemplate = render_template("login.html", errormessage = "Wrong username or password")
              

    return returntemplate




@app.route("/createinvoice", methods=["POST"])
def create_new_invoice():

    user = "elsa" # user id - from session data
    project_name = request.form["project_name"]  ## key to Project -name, not id
    client_name = request.form["client_name"] # connect to client name , not id
    summary = request.form["summary"]
    raised_date = datetime.now()
    due_date = request.form["due_date"]
    status = request.form["status"]
    tax_type = request.form["tax_type"] # connect to taxtype 
    discount = request.form["discount"]
    comment = request.form["comment"]

    sql = "INSERT INTO invoices (user, project_name, client_name, summary, raised_date, due_date, status, tax_type,discount,comment) VALUES (:user, :project_name, :client_name, :summary, :raised_date, :due_date, :status, :tax_type, :discount,:comment)"
    db.session.execute(text(sql), {"user":user,  "project_name": project_name, "client_name": client_name, "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,"comment":comment})
    db.session.commit()


    return render_template("create_invoice.html")


@app.route("/", methods=["POST"])
def new_invoice():
  
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





