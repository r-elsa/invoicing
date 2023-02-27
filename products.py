from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


def add_product(invoice,user_id,name,description,price_per_unit,amount):
   
    sql = "INSERT INTO products (invoice, user_id, name, description, price_per_unit, amount ) VALUES (:invoice, :user_id,"\
         ":name, :description, :price_per_unit, :amount )"
    db.session.execute(text(sql), {"invoice": invoice,"user_id": user_id,"name": name, "description": description, 
    "price_per_unit": price_per_unit,"amount": amount })
    db.session.commit()

def return_all(user_id):
    sql = "SELECT id, name FROM products WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    all_products = result.fetchall() 
    return all_products 




    