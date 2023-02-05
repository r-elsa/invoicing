
import app
db = app.db

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    
    def __init__(self, username,email,password ):
        self.username=username
        self.email= email
        self.password=password


class Client(db.Model):
    __tablename__= "clients"
    id = db.Column(db.Integer, primary_key =True)  ## client has many invoices
    name = db.Column(db.String(200))

    def __init__(self, name ):
        self.name= name
 

class Project(db.Model):
    __tablename__="projects"
    id = db.Column(db.Integer, primary_key =True) ##  project has many invoices, primary key to invoice that belongs to project
    name = db.Column(db.String(200), unique = True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name =name
        self.description = description
      

class Invoice(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key =True)
    logged_user = db.Column(db.Integer)  # user
    project_name = db.Column(db.String(200))  ## key to Project -name
    client_name = db.Column(db.String(200)) # connect to client
    summary = db.Column(db.String(200))
    raised_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(200))
    tax_type = db.Column(db.Integer)  # connect to taxtype 
    discount = db.Column(db.Float)
    comment = db.Column(db.String)
    
    def __init__(self, logged_user,project_name, client_name, summary, raised_date, due_date, status, tax_type, discount, comment):
        self.logged_user = logged_user
        self.project_name=project_name
        self.client_name=client_name
        self.summary=summary
        self.raised_date=raised_date
        self.due_date=due_date
        self.status=status
        self.tax_type=tax_type
        self.discount=discount
        self.comment=comment


class InvoiceItem(db.Model):
    __tablename__= "invoiceitems"
    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String(200))
    price_per_unit = db.Column(db.Float)
    amount = db.Column(db.Integer)


    def __init__(self, description, price_per_unit, amount):
        self.description = description
        self.price_per_unit= price_per_unit
        self.amount = amount

class TaxType(db.Model):
    __tablename__= "taxtypes"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(200))
    percentage = db.Column(db.Float)
    comment = db.Column(db.String(200))

    def __init__(self, name, percentage, comment):
        self.name = name
        self.percentage=percentage
        self.comment= comment

class Payment(db.Model):
    __tablename__= "payments"
    id = db.Column(db.Integer, primary_key =True)
    bank_name = db.Column(db.String(200))
    bank_branch = db.Column(db.String(200))
    invoice_id = db.Column(db.Integer ) # connect to invoice id
    comment = db.Column(db.String(200)) # 
  
  