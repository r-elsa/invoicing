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

  
@app.route("/")
def index():
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





