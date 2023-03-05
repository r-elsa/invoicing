from db import db
from db import db
from sqlalchemy import text


def create_invoice(user_id, project_id, client_id, summary, raised_date, due_date, status, tax_type, discount, comment, product_amount, final_price):
    sql = "INSERT INTO invoices (user_id, project_id, client_id, summary," \
          "raised_date, due_date, status, tax_type,discount,comment,product_amount, final_price) VALUES"\
          "(:user_id, :project_id, :client_id, :summary, :raised_date, :due_date, :status," \
          " :tax_type, :discount,:comment, :product_amount, :final_price)"
    
    db.session.execute(text(sql), {"user_id":user_id,  "project_id": project_id, "client_id": client_id, 
    "summary":summary, "raised_date":raised_date, "due_date":due_date, "status":status, "tax_type": tax_type,"discount":discount,
    "comment":comment, "product_amount": product_amount, "final_price":final_price})

    db.session.commit()
   

def return_all(user_id):
    sql = "SELECT I.id, I.project_id, I.client_id, I.due_date, I.status, I.final_price, C.name AS client_name, P.name AS project_name FROM invoices I LEFT JOIN clients C ON C.id = I.client_id LEFT JOIN projects P ON P.id = I.project_id WHERE I.user_id =:user_id" \
    " ORDER BY id DESC"
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall() 

def return_all_admin():
    sql = "SELECT U.id AS userid, U.username, U.email, I.id, P.name as project_name, C.name AS client_name, I.due_date, I.status, I.final_price" \
    " FROM invoices I LEFT JOIN users U ON U.id = I.user_id LEFT JOIN clients C ON C.id = I.client_id LEFT JOIN projects P ON P.id = I.project_id"  \
    " ORDER BY userid, I.id"
    result = db.session.execute(text(sql))
    return result.fetchall() 


def return_status(id):
    sql = "SELECT id, status FROM invoices WHERE id =:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchone() 



def count_rows(user_id):
    sql = "SELECT COUNT(*) FROM invoices WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchone() 
   

def filter_by_client(user_id, client_id):
    sql = "SELECT I.id, I.project_id, I.client_id, I.due_date, I.status, I.final_price, C.name AS client_name, P.name AS project_name FROM invoices I LEFT JOIN clients C ON C.id = I.client_id LEFT JOIN projects P ON P.id = I.project_id" \
          " WHERE I.user_id = :user_id AND I.client_id =:client_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "client_id":client_id })
    return result.fetchall()

def filter_by_project(user_id, project_id):
    sql = "SELECT I.id, I.project_id, I.client_id, I.due_date, I.status, I.final_price, P.name AS project_name, C.name AS client_name FROM invoices I LEFT JOIN projects P ON P.id = I.project_id LEFT JOIN clients C ON C.id = I.client_id" \
          " WHERE I.user_id = :user_id AND I.project_id =:project_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "project_id":project_id })
    return result.fetchall()


def delete(user_id, id):
    sql = "DELETE FROM invoices WHERE user_id =:user_id AND id = :id"
    db.session.execute(text(sql), {"user_id":user_id, "id":id })
    db.session.commit()

def admin_delete(id):
    sql = "DELETE FROM invoices WHERE id = :id"
    db.session.execute(text(sql), {"id":id })
    db.session.commit()

def update_status(user_id, id, status):
    sql = "UPDATE invoices SET status=:status WHERE user_id=:user_id and id=:id"
    db.session.execute(text(sql), {"status":status,"user_id":user_id, "id":id })
    db.session.commit()

def admin_update_status(id, status):
    sql = "UPDATE invoices SET status=:status WHERE id=:id"
    db.session.execute(text(sql), {"status":status, "id":id })
    db.session.commit()

def get_sum(user_id):
    sql = "SELECT SUM(final_price) FROM invoices WHERE user_id =:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchone()


