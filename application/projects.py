from db import db
from sqlalchemy import text


def add_project(name, description, user_id):
    sql = "INSERT INTO projects (name, description, user_id) VALUES (:name, :description, :user_id)"
    db.session.execute(text(sql), {"name": name, "description": description, "user_id":user_id})
    db.session.commit()

def check_project(user_id, name):
    sql = "SELECT id, name FROM projects WHERE user_id =:user_id AND name =:name"
    result = db.session.execute(text(sql), {"user_id":user_id,"name":name})
    project = result.fetchone() 
    if project is None:
        return False
    return True 



def return_all(user_id):
    sql = "SELECT id, name FROM projects WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    all_projects = result.fetchall() 
    return all_projects 
