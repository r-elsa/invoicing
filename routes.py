from app import app
from flask import redirect, render_template, request, session, abort
from datetime import datetime
import secrets
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
    noinvoices = True

    if request.method == "POST":
        if referralroute[-6:] =="signup":
            session["csrf_token"] = secrets.token_hex(16)
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
        
            soughtuser = users.check_signup(username)
            if soughtuser:
                return render_template("signup.html", error_message="Username already taken")
          
            else:       
                users.create_user(username, email, password)
                logged_user = users.get_user_id(username)
                session["logged_user"] = logged_user
                session["username"] = username
            

        if referralroute[-5:] == "login":
            session["csrf_token"] = secrets.token_hex(16)
            username = request.form["username"]
            password = request.form["password"]
            
            (soughtuser, logged_user) = users.check_login(username, password)
            if not soughtuser:
                return render_template("login.html", error_message="Wrong username or password")
            
            else:
                session["logged_user"] = logged_user
                session["username"] = username

   
        if referralroute[-13:] == "createinvoice":
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
            #final_price_string = "{:.2f}".format(final_price)
            
            invoices.create_invoice(logged_user, project_name, client_name, summary, raised_date, due_date, status, tax_type, discount, comment, product_amount, final_price)

        
        if "update" in referralroute:
            user_id = session["logged_user"]
            invoice_id = request.form["id"]
            status = request.form["status"]
            invoices.update_status(user_id, invoice_id, status)
    


    logged_user = session["logged_user"] 
    username = session["username"]
    all_invoices = invoices.return_all(logged_user)
    sumofinvoices = invoices.get_sum(logged_user)
    print(sumofinvoices)

    if invoices.count_rows(logged_user)[0] > 0:
        noinvoices = False
    return render_template("dashboard.html", all_invoices=all_invoices, username=username, noinvoices=noinvoices)

@app.route("/createinvoice", methods=["GET","POST"])
def create_new_invoice():
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

        referralroute = request.referrer
        if referralroute[-10:] =="addproduct":
            invoice = None
            user_id = session["logged_user"]
            product_name = request.form["name"]  
            description = request.form["description"] 
            price = request.form["price"]
            product_already_exists = products.check_product(user_id, product_name)
            if product_already_exists:
                return render_template("add_product.html", error_message="Product with same name already exists")     
            products.add_product(invoice, user_id, product_name, description, price)
        

        if referralroute[-9:]=="addclient":
            client_name =  request.form["name"] 
            client_phone =  request.form["phone"] 
            client_email =  request.form["email"] 
            client_description = request.form["description"] 
            user_id = session["logged_user"]

            client_already_exists = clients.check_client(user_id, client_name)
            if client_already_exists:
                return render_template("add_client.html", error_message="Client with same name already exists")
         
            clients.add_client(client_name, client_phone, client_email, client_description, user_id)
        
        if referralroute[-10:] == "addproject":
            user_id = session["logged_user"]
            project_name = request.form["name"] 
            project_description = request.form["description"]
            project_already_exists = projects.check_project(user_id, project_name)
            if project_already_exists:
                return render_template("add_project.html", error_message="Project with same name already exists")


            projects.add_project(project_name, project_description, user_id)


    logged_user = session["logged_user"] 
    all_products = products.return_all(logged_user)
    all_clients = clients.return_all(logged_user)
    all_projects = projects.return_all(logged_user)
    
    return render_template("create_invoice.html", products=all_products, clients=all_clients, projects=all_projects)
 

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
        return render_template("extended_filtering.html", clients=all_clients, projects=all_projects,filtered_invoices=False)
          
    

@app.route("/filterbyclient", methods = ["POST"])
def filter_by_client():
     if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

        logged_user = session["logged_user"] 
        chosen_client = request.form["client"]
        filtered_invoices = False
        if chosen_client:
            invoices_chosen_client = invoices.filter_by_client(logged_user, chosen_client)
        
        if len(invoices_chosen_client)>0:
            filtered_invoices=True
        
        all_clients = clients.return_all(logged_user)
        all_projects = projects.return_all(logged_user)
        return render_template("extended_filtering.html", clients=all_clients, projects=all_projects,invoices=invoices_chosen_client,filtered_invoices=filtered_invoices) 


@app.route("/filterbyproject", methods = ["POST"])
def filter_by_project():
     if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        logged_user = session["logged_user"] 
        chosen_project = request.form["project"][0]
        
        filtered_invoices = False
        if chosen_project:
            invoices_chosen_project = invoices.filter_by_project(logged_user, chosen_project)
        if len(invoices_chosen_project)>0:
            filtered_invoices=True
        
        all_clients = clients.return_all(logged_user)
        all_projects = projects.return_all(logged_user)
          
        return render_template("extended_filtering.html",clients=all_clients, projects=all_projects, invoices=invoices_chosen_project, filtered_invoices = filtered_invoices) 


@app.route("/delete/<id>")
def delete(id):
    if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
    logged_user = session["logged_user"] 
    invoices.delete(logged_user, id)
    return redirect("/dashboard")


@app.route("/update/<id>")
def modify(id):
    if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
    logged_user = session["logged_user"] 
    status = invoices.return_status(logged_user, id)[1]
    return render_template("update_invoice.html", invoice_id=id, status=status)
    

@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")
