from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timezone
from db import db
import users
import invoices

  
@app.route("/")
def index():
    return redirect('/login')

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup",  methods=["POST"])
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

    if request.method == "POST":
    # sign up
        if referralroute[-6:]=="signup":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            #if username alredy taken
        
            soughtuser = users.check_signup(username)
            
            if (len(soughtuser)) > 0:
                error = True
                returntemplate = "signup.html"
                error_message = "Username already taken"
            #username not taken"
            else:     
                
                users.create_user(username,email,password)

                logged_user = users.get_user_id(username)
                session["logged_user"] = logged_user
            

    
    #login
        elif referralroute[-5:]=="login":
            username = request.form["username"]
            password = request.form["password"]

            username = "meme"
            password ="mememe"
            
            soughtuser = users.check_login(username,password)
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

            invoices.create_invoice(logged_user,project_name,client_name,summary, raised_date, due_date, status, tax_type, discount, comment, productprice, product_amount)

 

    all_invoices = invoices.return_all(logged_user)

    if error == True:
        return render_template(returntemplate, error_message = error_message)
    else:
        return render_template("dashboard.html", all_invoices=all_invoices, username=username)


@app.route("/createinvoice", methods=["GET"])
def create_new_invoice():
    return render_template("create_invoice.html")


@app.route("/products", methods=["GET"])
def view_products():
    return render_template("products.html")


@app.route("/createproduct", methods=["GET"])
def create_new_product():
    return render_template("create_product.html")


@app.route("/clients", methods=["GET"])
def view_clients():
    return render_template("clients.html") 





@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")
