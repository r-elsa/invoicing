from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


def add_product(invoice, user_id, name, description, price):
   
    sql = "INSERT INTO products (invoice, user_id, name, description, price ) VALUES (:invoice, :user_id,"\
         ":name, :description, :price )"
    db.session.execute(text(sql), {"invoice": invoice,"user_id": user_id,"name": name, "description": description, 
    "price": price })
    db.session.commit()

def get_product_price(name):
    sql = "SELECT id, price FROM products WHERE name =:name"
    result = db.session.execute(text(sql), {"name":name})
    price = result.fetchone() 
    return price 

def return_all(user_id):
    sql = "SELECT id, name FROM products WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    all_products = result.fetchall() 
    return all_products 




    