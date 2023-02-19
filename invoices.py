from db import db
from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



def create_invoice(logged_user,project_name,client_name,summary, raised_date, due_date, status, tax_type, discount, comment, product_amount):
    sql = "INSERT INTO invoices (logged_user, project_name, client_name, summary, raised_date, due_date, status, tax_type,discount,comment,product_amount) VALUES (:logged_user, :project_name, :client_name, :summary, :raised_date, :due_date, :status, :tax_type, :discount,:comment, :product_amount)"
    db.session.execute(text(sql), {"logged_user":logged_user,  "project_name": project_name, "client_name": client_name, "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,"comment":comment, "product_amount": product_amount})
    db.session.commit()
   



def return_all(logged_user):
    sql = "SELECT id, project_name, client_name, due_date, status FROM invoices WHERE logged_user =:logged_user"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    all_invoices = result.fetchall() 
    return all_invoices 
