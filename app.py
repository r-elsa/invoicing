from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import re
from models import User, Client, Project, Invoice,InvoiceItem, TaxType, Payment

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    db.create_all()
    return render_template("login.html")

@app.route("/signup",  methods=["POST", "GET"])
def signup():
    return render_template("signup.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():      
    referralroute = request.referrer
   
    # create invoice
    if referralroute[-13:]=="createinvoice":
        logged_user = 2 # user id - from session data
        project_name = request.form["project_name"]  ## key to Project -name, not id
        client_name = request.form["client_name"] # connect to client name , not id
        summary = request.form["summary"]
        raised_date = datetime.now()
        due_date = request.form["due_date"]
        status = request.form["status"]
        tax_type = request.form["tax_type"] # connect to taxtype 
        discount = request.form["discount"]
        comment = request.form["comment"]
       
        sql = "INSERT INTO invoices (logged_user, project_name, client_name, summary, raised_date, due_date, status, tax_type,discount,comment) VALUES (:logged_user, :project_name, :client_name, :summary, :raised_date, :due_date, :status, :tax_type, :discount,:comment)"
        db.session.execute(text(sql), {"logged_user":logged_user,  "project_name": project_name, "client_name": client_name, "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,"comment":comment})
        db.session.commit()
     
    # sign up
    elif referralroute[-6:]=="signup":
        username = request.form["username"]
        password = request.form["password"]
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
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, email FROM users WHERE username LIKE :username AND password LIKE :password"
        result = db.session.execute(text(sql), {"username":"%"+username+"%", "password":"%"+password+"%"})
        soughtuser = result.fetchall()
        if (len(soughtuser)) == 0:
            render_template("login.html", errormessage = "Wrong username or password")

    logged_user = 2 
    sql = "SELECT id, project_name, client_name, due_date, status FROM invoices WHERE logged_user =:logged_user"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    all_invoices = result.fetchall()      
    return render_template("dashboard.html", all_invoices=all_invoices)


@app.route("/createinvoice", methods=["POST"])
def create_new_invoice():
    return render_template("create_invoice.html")

@app.route("/", methods=["POST"])
def new_invoice():
  
    service = request.form["service"]
    taxpercentage = request.form.getlist("taxpercentage")
    message = request.form["message"]
   
    return render_template("invoice.html", service = service,
                                            taxpercentage = taxpercentage,
                                            message=message
    )

@app.route("/dashboard/invoice/<int:id>")
def page3(id):
    return "This is invoice number " + str(id)

if __name__ == '__main__':
    app.run(debug=True)





