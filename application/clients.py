from db import db
from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

def add_client(name, phone, email, description, user_id):
    sql = "INSERT INTO clients (name, phone, email, description, user_id) VALUES (:name, :phone, :email, :description, :user_id)"
    db.session.execute(text(sql), {"name":name,"phone":phone,"email":email,"description":description,"user_id":user_id})
    db.session.commit()

def check_client(user_id, name):
    sql = "SELECT id, name FROM clients WHERE user_id =:user_id AND name =:name"
    result = db.session.execute(text(sql), {"user_id":user_id,"name":name})
    client = result.fetchone() 
    if client is None:
        return False
    return True 

def return_all(user_id):
    sql = "SELECT id, name FROM clients WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    all_clients = result.fetchall() 
    return all_clients 

  
  