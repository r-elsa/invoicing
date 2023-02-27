from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash


def check_login(username,password):
    sql = "SELECT id, username, password FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    user = result.fetchone()
 
      
    if not user:
        return (False, 1000)
    else:
        if check_password_hash(user[2], password):
            return (True,user[0])
        else:
            return (False, 1000)
   
   
     


def check_signup(username):
    sql = "SELECT id, username FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    soughtuser = result.fetchall()
    return soughtuser


def create_user(username,email,password):
    password_hashed = generate_password_hash(password)
    sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
    db.session.execute(text(sql), {"username":username, "email":email,"password":password_hashed})
    db.session.commit()


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    logged_user= result.fetchall()[0][0]
    return logged_user