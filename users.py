from db import db
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


def check_login(username,password):
    sql = "SELECT id, email FROM users WHERE username LIKE :username AND password LIKE :password"
    result = db.session.execute(text(sql), {"username":"%"+username+"%", "password":"%"+password+"%"})
    soughtuser = result.fetchall()
    return soughtuser

def check_signup(username):
    sql = "SELECT id, username FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    soughtuser = result.fetchall()
    return soughtuser


def create_user(username,email,password):
    sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
    db.session.execute(text(sql), {"username":username, "email":email,"password":password})
    db.session.commit()


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    logged_user= result.fetchall()[0][0]
    return logged_user