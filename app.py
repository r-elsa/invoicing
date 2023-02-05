from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from os import getenv
from datetime import datetime, timezone
import re


load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY") #secret key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # database url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    id = db.Column(db.Integer, primary_key =True)  
    name = db.Column(db.String(200))

    def __init__(self, name ):
        self.name= name
 

class Project(db.Model):
    __tablename__="projects"
    id = db.Column(db.Integer, primary_key =True) 
    name = db.Column(db.String(200), unique = True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name =name
        self.description = description
      

class Invoice(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key =True)
    logged_user = db.Column(db.Integer) 
    project_name = db.Column(db.String(200))  
    client_name = db.Column(db.String(200)) 
    summary = db.Column(db.String(200))
    raised_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(200))
    tax_type = db.Column(db.Integer)  
    discount = db.Column(db.Float)
    comment = db.Column(db.String)
    productprice = db.Column(db.Float)
    product_amount = db.Column(db.Integer)
    
    def __init__(self, logged_user,project_name, client_name, summary, raised_date, due_date, status, tax_type, discount, comment, productprice, product_amount):
        self.logged_user = logged_user
        self.project_name=project_name
        self.client_name=client_name
        self.summary=summary
        self.raised_date=raised_date
        self.due_date=due_date
        self.status=status
        self.tax_type=tax_type
        self.discount=discount
        self.comment=comment
        self.productprice = productprice
        self.product_amount=product_amount


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
    invoice_id = db.Column(db.Integer ) 
    comment = db.Column(db.String(200)) 
  
  

@app.route("/")
def index():
    db.create_all()
    return redirect('/login')

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup",  methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route("/dashboard", methods=["GET","POST"])
def dashboard():      
    referralroute = request.referrer
    logged_user = 1000000
    username = "placeholder"
    error = False 
    returntemplate = ""
    error_message = ""  

    # sign up
    if referralroute[-6:]=="signup":
        username = request.form["username"]
        password = request.form["password"]

        #if username alredy taken
        sql = "SELECT id, username FROM users WHERE username LIKE :username"
        result = db.session.execute(text(sql), {"username":"%"+username+"%"})
        soughtuser = result.fetchall()
        if (len(soughtuser)) > 0:
            error = True
            returntemplate = "signup.html"
            error_message = "Username already taken"
        #username not taken"
        else:     
            email = request.form["email"]
            sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
            db.session.execute(text(sql), {"username":username, "email":email,"password":password})
            db.session.commit()

            sql = "SELECT id FROM users WHERE username LIKE :username"
            result = db.session.execute(text(sql), {"username":"%"+username+"%"})
            logged_user= result.fetchall()[0][0]
            session["logged_user"] = logged_user
         
    
    #login
    elif referralroute[-5:]=="login":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, email FROM users WHERE username LIKE :username AND password LIKE :password"
        result = db.session.execute(text(sql), {"username":"%"+username+"%", "password":"%"+password+"%"})
        soughtuser = result.fetchall()
        if (len(soughtuser)) == 0:
            error = True
            returntemplate = "login.html"
            error_message = "Wrong username or password"
           
        else:
            logged_user = soughtuser[0][0]
            session["logged_user"] = logged_user

    # create invoice
    elif referralroute[-13:]=="createinvoice":
        logged_user=session["logged_user"]
      

        project_name = request.form["project_name"]  
        client_name = request.form["client_name"] 
        summary = request.form["summary"]
        raised_date = datetime.now()
        due_date = request.form["due_date"]
        status = request.form["status"]
        tax_type = request.form["tax_type"] 
        discount = request.form["discount"]
        comment = request.form["comment"]
        productprice = float(request.form["productprice"])
        product_amount = int(request.form["product_amount"])

      

        sql = "INSERT INTO invoices (logged_user, project_name, client_name, summary, raised_date, due_date, status, tax_type,discount,comment,productprice,product_amount) VALUES (:logged_user, :project_name, :client_name, :summary, :raised_date, :due_date, :status, :tax_type, :discount,:comment, :productprice, :product_amount)"
        db.session.execute(text(sql), {"logged_user":logged_user,  "project_name": project_name, "client_name": client_name, "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,"comment":comment, "productprice": productprice, "product_amount": product_amount})
        db.session.commit()
     

    
    sql = "SELECT id, project_name, client_name, due_date, status FROM invoices WHERE logged_user =:logged_user"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    all_invoices = result.fetchall()  

    if error == True:
        return render_template(returntemplate, error_message = error_message)
    else:
        return render_template("dashboard.html", all_invoices=all_invoices, username=username)


@app.route("/createinvoice", methods=["GET","POST"])
def create_new_invoice():
    return render_template("create_invoice.html")



@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)





