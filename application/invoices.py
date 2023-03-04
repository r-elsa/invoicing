from db import db
from db import db
from sqlalchemy import text


def create_invoice(logged_user, project_name, client_name, summary, raised_date, due_date, status, tax_type, discount, comment, product_amount, final_price):
    sql = "INSERT INTO invoices (logged_user, project_name, client_name, summary," \
          "raised_date, due_date, status, tax_type,discount,comment,product_amount, final_price) VALUES"\
          "(:logged_user, :project_name, :client_name, :summary, :raised_date, :due_date, :status," \
          " :tax_type, :discount,:comment, :product_amount, :final_price)"
    
    db.session.execute(text(sql), {"logged_user":logged_user,  "project_name": project_name, "client_name": client_name, 
    "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,
    "comment":comment, "product_amount": product_amount, "final_price":final_price})

    db.session.commit()
   

def return_all(logged_user):
    sql = "SELECT id, project_name, client_name, due_date, status, final_price FROM invoices WHERE logged_user =:logged_user" \
    " ORDER BY id DESC LIMIT 10"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    return result.fetchall() 

def return_status(logged_user, id):
    sql = "SELECT id, status FROM invoices WHERE logged_user =:logged_user AND id =:id"
    result = db.session.execute(text(sql), {"logged_user":logged_user, "id":id})
    return result.fetchone() 



def count_rows(logged_user):
    sql = "SELECT COUNT(*) FROM invoices WHERE logged_user =:logged_user"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    return result.fetchone() 
   

def filter_by_client(logged_user, client):
    sql = "SELECT I.id, I.project_name, I.client_name, I.due_date, I.status, I.final_price FROM invoices I, users U" \
          " WHERE I.logged_user = U.id AND I.logged_user =:logged_user AND I.client_name =:client"
    result = db.session.execute(text(sql), {"logged_user":logged_user, "client":client })
    return result.fetchall()

def filter_by_project(logged_user, project_name):
    sql = "SELECT I.id, I.project_name, I.client_name, I.due_date, I.status, I.final_price FROM invoices I" \
          " WHERE I.logged_user = :logged_user AND I.project_name =:project_name"
    result = db.session.execute(text(sql), {"logged_user":logged_user, "project_name":project_name })
    return result.fetchall()


def delete(logged_user, id):
    sql = "DELETE FROM invoices WHERE logged_user =:logged_user AND id = :id"
    db.session.execute(text(sql), {"logged_user":logged_user, "id":id })
    db.session.commit()

def update_status(logged_user, id, status):
    sql = "UPDATE invoices SET status=:status WHERE logged_user=:logged_user and id=:id"
    db.session.execute(text(sql), {"status":status,"logged_user":logged_user, "id":id })
    db.session.commit()

def get_sum(logged_user):
    sql = "SELECT SUM(final_price) FROM invoices WHERE logged_user =:logged_user"
    result = db.session.execute(text(sql), {"logged_user":logged_user})
    return result.fetchone()

""" EXEMPEL:
sql = "SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id"
     """

