from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timezone
from db import db
import users
import invoices
import products
import clients

  
@app.route("/")
def index():
    return redirect('/login')

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup",  methods=["GET"])
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
    noinvoices = False

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



        elif referralroute[-10:]=="addproduct":
         
            invoice = None
            user_id = session["logged_user"]
            product_name = request.form["name"]  
            description = request.form["description"] 
            priceperunit = request.form["priceperunit"]
            amount = 0
            products.add_product(invoice,user_id,product_name,description,priceperunit,amount)
        

        elif referralroute[-9:]=="addclient":
            client_name =  request.form["name"] 
            client_phone =  request.form["phone"] 
            client_email =  request.form["email"] 
            client_description =  request.form["description"] 
            user_id = session["logged_user"]
            clients.add_client(client_name,client_phone,client_email, client_description, user_id)
        



    logged_user = session["logged_user"] 
    all_invoices = invoices.return_all(logged_user)


    if len(all_invoices)==0:
        noinvoices = True
    

    if error == True:
        return render_template(returntemplate, error_message = error_message)
    else:
        return render_template("dashboard.html", all_invoices=all_invoices, username=username, noinvoices=noinvoices)


@app.route("/createinvoice", methods=["GET"])
def create_new_invoice():
    logged_user = session["logged_user"] 
    all_products = products.return_all(logged_user)
    all_clients = clients.return_all(logged_user)
    return render_template("create_invoice.html", products = all_products, clients = all_clients)

 

@app.route("/addproduct", methods=["GET", "POST"])
def add_new_product():
    return render_template("add_product.html")


@app.route("/addclient", methods=["GET"])
def add_new_clients():
    return render_template("add_client.html") 



@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")
