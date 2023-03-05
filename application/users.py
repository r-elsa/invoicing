from db import db
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash


def check_login(username, password):
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
    soughtuser = result.fetchone()
    return soughtuser


def create_user(username, email, password, admin):
    password_hashed = generate_password_hash(password)
    sql = "INSERT INTO users (username, email, password, admin) VALUES (:username, :email, :password, :admin)"
    db.session.execute(text(sql), {"username":username, "email":email,"password":password_hashed, "admin":admin})
    db.session.commit()


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    user_id= result.fetchall()[0][0]
    return user_id

def is_admin(username):
    sql = "SELECT admin FROM users WHERE username LIKE :username"
    result = db.session.execute(text(sql), {"username":"%"+username+"%"})
    user_id= result.fetchall()[0][0]
    return user_id
