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


@app.route("/signup")
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
            admin = False
        
            soughtuser = users.check_signup(username)
            if soughtuser:
                return render_template("signup.html", error_message="Username already taken")
          
            else:       
                users.create_user(username, email, password, admin)
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
        
        if "dashboard" in referralroute:
            return redirect("/login")

   
        if referralroute[-13:] == "createinvoice":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            user_id = session["logged_user"]
            project_id = request.form["project_id"]  
            client_id = request.form["client_id"] 
            summary = request.form["summary"]
            raised_date = datetime.now()
            due_date = request.form["due_date"]
            status = request.form["status"]
            tax_type = int(request.form["tax_type"])
            discount = int(request.form["discount"])
            comment = request.form["comment"]
            product_id = request.form['product']
            product_price = products.get_product_price(product_id)[1]
            product_amount = int(request.form["product_amount"])
         
            final_price = ((product_price*product_amount))*(1-((discount)/100))*(1-((tax_type/100)))
                  
            invoices.create_invoice(user_id, project_id, client_id, summary, raised_date, due_date, status, tax_type, discount, comment, product_amount, final_price)

        
        if "update" in referralroute:
            username = session["username"] 
            user_id = session["logged_user"]
            invoice_id = request.form["id"]
            status = request.form["status"]
            if users.is_admin(username):
                status = invoices.admin_update_status(invoice_id, status)
            else:
                invoices.update_status(user_id, invoice_id, status)
    
   
    current_user = session["logged_user"] 
    username = session["username"]
    all_invoices = invoices.return_all(current_user)
 
   

    if invoices.count_rows(current_user)[0] > 0:
        noinvoices = False

    isadmin = False
    if users.is_admin(username):
        isadmin = True
        all_invoices = invoices.return_all_admin()
        noinvoices = False
        if len(all_invoices) ==0:
             noinvoices=True
       
    return render_template("dashboard.html", all_invoices=all_invoices, username=username, noinvoices=noinvoices, isadmin=isadmin)

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
                session['errormessage'] = "Product with same name already exists"
                return redirect("/addproduct")
         
            products.add_product(invoice, user_id, product_name, description, price)
        

        if referralroute[-9:]=="addclient":
            client_name =  request.form["name"] 
            client_phone =  request.form["phone"] 
            client_email =  request.form["email"] 
            client_description = request.form["description"] 
            user_id = session["logged_user"]

            client_already_exists = clients.check_client(user_id, client_name)
            if client_already_exists:
                session['errormessage'] = "Client with same name already exists"
                return redirect("/addclient")
         
            clients.add_client(client_name, client_phone, client_email, client_description, user_id)
        
        if referralroute[-10:] == "addproject":
            user_id = session["logged_user"]
            project_name = request.form["name"] 
            project_description = request.form["description"]
            project_already_exists = projects.check_project(user_id, project_name)
            if project_already_exists:
                session['errormessage'] = "Project with same name already exists"
                return redirect("/addproject")
      
            projects.add_project(project_name, project_description, user_id)

    current_user = session["logged_user"] 
    all_products = products.return_all(current_user)
    all_clients = clients.return_all(current_user)
    all_projects = projects.return_all(current_user)
    
    return render_template("create_invoice.html", products=all_products, clients=all_clients, projects=all_projects)
 

@app.route("/addproduct", methods=["GET"])
def add_new_product():
    errormessage = ''
    if session.get('errormessage'):
        errormessage = session['errormessage'] 
        session.pop('errormessage')
    return render_template("add_product.html", errormessage=errormessage)


@app.route("/addclient", methods=["GET"])
def add_new_client():
    errormessage = ''
    if session.get('errormessage'):
        errormessage = session['errormessage'] 
        session.pop('errormessage')
    return render_template("add_client.html", errormessage=errormessage) 

@app.route("/addproject", methods=["GET"])
def add_new_project():
    errormessage = ''
    if session.get('errormessage'):
        errormessage = session['errormessage'] 
        session.pop('errormessage')
    return render_template("add_project.html", errormessage=errormessage)


@app.route("/filter", methods = ["GET"])
def filter():
    current_user = session["logged_user"] 
    if request.method == "GET":
        all_clients = clients.return_all(current_user)
        all_projects = projects.return_all(current_user)
        return render_template("extended_filtering.html", clients=all_clients, projects=all_projects,filtered_invoices=False)
          
    

@app.route("/filterbyclient", methods = ["GET"])
def filter_by_client():
     if request.method == "GET":
        if session["csrf_token"] != request.args["csrf_token"]:
                abort(403)

        current_user = session["logged_user"] 
        chosen_client = request.args["client"]
        filtered_invoices = False
        if chosen_client:
            invoices_chosen_client = invoices.filter_by_client(current_user, chosen_client)
        
        if len(invoices_chosen_client)>0:
            filtered_invoices=True
        
        all_clients = clients.return_all(current_user)
        all_projects = projects.return_all(current_user)
        return render_template("extended_filtering.html", clients=all_clients, projects=all_projects,invoices=invoices_chosen_client,filtered_invoices=filtered_invoices) 


@app.route("/filterbyproject", methods = ["GET"])
def filter_by_project():
     if request.method == "GET":
        if session["csrf_token"] != request.args["csrf_token"]:
                abort(403)
        current_user = session["logged_user"] 
        chosen_project_id = request.args["project"]
        
        filtered_invoices = False
        if chosen_project_id:
            invoices_chosen_project = invoices.filter_by_project(current_user, chosen_project_id)
        if len(invoices_chosen_project)>0:
            filtered_invoices=True
        
        all_clients = clients.return_all(current_user)
        all_projects = projects.return_all(current_user)
          
        return render_template("extended_filtering.html",clients=all_clients, projects=all_projects, invoices=invoices_chosen_project, filtered_invoices = filtered_invoices) 


@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
    current_user = session["logged_user"] 
    
    username = session["username"] 

    if users.is_admin(username):
        invoices.admin_delete(id)
    else:
         invoices.delete(current_user, id)
    return redirect("/dashboard")




@app.route("/update/<int:id>", methods=["POST"])
def modify(id):
    if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

    status = invoices.return_status(id)[1]
    return render_template("update_invoice.html", invoice_id=id, status=status)

  

@app.route("/logout")
def logout():
    del session["logged_user"]
    return redirect("/login")
