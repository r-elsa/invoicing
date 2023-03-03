from app import app
from flask import Flask
from flask import redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timezone
import secrets
from db import db
import users
import invoices
import products
import clients
import projects

  
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
    noinvoices = True

    if request.method == "POST":
        if referralroute[-6:]=="signup":
            session["csrf_token"] = secrets.token_hex(16)
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
        
            soughtuser= users.check_signup(username)
            if soughtuser:
                returntemplate = "signup.html"
                error_message = "Username already taken"
          
            else:       
                users.create_user(username,email,password)
                logged_user = users.get_user_id(username)
                session["logged_user"] = logged_user
            

        elif referralroute[-5:]=="login":
            session["csrf_token"] = secrets.token_hex(16)
            username = request.form["username"]
            password = request.form["password"]
            
            (soughtuser, logged_user) = users.check_login(username,password)
            if not soughtuser:
                error = True
                returntemplate = "login.html"
                error_message = "Wrong username or password"
            
            else:
                session["logged_user"] = logged_user

   
        elif referralroute[-13:]=="createinvoice":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            logged_user=session["logged_user"]
            project_name = request.form["project_name"]  
            client_name = request.form["client_name"] 
            summary = request.form["summary"]
            raised_date = datetime.now()
            due_date = request.form["due_date"]
            status = request.form["status"]
            tax_type = int(request.form["tax_type"])
            discount = int(request.form["discount"])
            comment = request.form["comment"]
            product_name = request.form['product']
            product_price = products.get_product_price(product_name)[1]
            product_amount = int(request.form["product_amount"])
         
            final_price = ((product_price*product_amount))*(1-((discount)/100))*(1-((tax_type/100)))
            final_price_string = "{:.2f}".format(final_price)
            
            invoices.create_invoice(logged_user,project_name,client_name,summary, raised_date, due_date, status, tax_type, discount, comment, product_amount, final_price_string)

        elif referralroute[-10:]=="addproduct":
            invoice = None
            user_id = session["logged_user"]
            product_name = request.form["name"]  
            description = request.form["description"] 
            price = request.form["price"]
            products.add_product(invoice,user_id,product_name,description,price)
        

        elif referralroute[-9:]=="addclient":
            client_name =  request.form["name"] 
            client_phone =  request.form["phone"] 
            client_email =  request.form["email"] 
            client_description =  request.form["description"] 
            user_id = session["logged_user"]
            clients.add_client(client_name,client_phone,client_email, client_description, user_id)
        
        elif referralroute[-10:]=="addproject":
            user_id = session["logged_user"]
            project_name =  request.form["name"] 
            project_description =  request.form["description"] 
            projects.add_project(project_name, project_description, user_id)
        
    
    logged_user = session["logged_user"] 
    all_invoices = invoices.return_all(logged_user)


    if error == True:
        return render_template(returntemplate, error_message = error_message)
    else:
     
        if invoices.count_rows(logged_user)[0] >0:
            noinvoices = False
        return render_template("dashboard.html", all_invoices=all_invoices, username=username, noinvoices=noinvoices)

@app.route("/createinvoice", methods=["GET", "POST"])
def create_new_invoice():
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

        referralroute = request.referrer
        if referralroute[-10:]=="addproduct":
            invoice = None
            user_id = session["logged_user"]
            product_name = request.form["name"]  
            description = request.form["description"] 
            price = request.form["price"]
            products.add_product(invoice,user_id,product_name,description,price)
        

        elif referralroute[-9:]=="addclient":
            client_name =  request.form["name"] 
            client_phone =  request.form["phone"] 
            client_email =  request.form["email"] 
            client_description =  request.form["description"] 
            user_id = session["logged_user"]
            clients.add_client(client_name,client_phone,client_email, client_description, user_id)
        
        elif referralroute[-10:]=="addproject":
            user_id = session["logged_user"]
            project_name =  request.form["name"] 
            project_description =  request.form["description"] 
     
            projects.add_project(project_name, project_description, user_id)



    logged_user = session["logged_user"] 
    all_products = products.return_all(logged_user)
    if len(all_products)==0:
        noproducts=True
    all_clients = clients.return_all(logged_user)
    all_projects = projects.return_all(logged_user)
      
    
    return render_template("create_invoice.html", products = all_products, clients = all_clients, projects = all_projects)

 

@app.route("/addproduct", methods=["GET", "POST"])
def add_new_product():
    return render_template("add_product.html")


@app.route("/addclient", methods=["GET"])
def add_new_client():
    return render_template("add_client.html", action ="createinvoice") 

@app.route("/addproject", methods=["GET"])
def add_new_project():
    return render_template("add_project.html")


@app.route("/filter", methods = ["GET"])
def filter():
    logged_user = session["logged_user"] 
    if request.method == "GET":
        all_clients = clients.return_all(logged_user)
        all_projects = projects.return_all(logged_user)
        return render_template("extended_filtering.html", clients = all_clients, projects=all_projects, noinvoices=True)
          
    

@app.route("/filterbyclient", methods = ["POST"])
def filter_by_client():
     if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        logged_user = session["logged_user"] 
        
        chosen_client = request.form["client"]
        if chosen_client:
            invoices_chosen_client = invoices.filter_by_client(logged_user,chosen_client)
        
        all_clients = clients.return_all(logged_user)
        all_projects = projects.return_all(logged_user)
        return render_template("extended_filtering.html", clients = all_clients, projects=all_projects,invoices = invoices_chosen_client, noinvoices=False) 


@app.route("/filterbyproject", methods = ["POST"])
def filter_by_project():
     if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        logged_user = session["logged_user"] 

        chosen_project = request.form["project"]
       
        if chosen_project:
            invoices_chosen_project = invoices.filter_by_project(logged_user,chosen_project)
            print(invoices_chosen_project)
        
        all_clients = clients.return_all(logged_user)
        all_projects = projects.return_all(logged_user)
          
        return render_template("extended_filtering.html",clients = all_clients, projects=all_projects, invoices = invoices_chosen_project, noinvoices=False) 





@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")
