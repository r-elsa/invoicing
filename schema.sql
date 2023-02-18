CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    email TEXT,
    password TEXT

);


CREATE TABLE clients (
    id SERIAL PRIMARY KEY, 
    client_name TEXT UNIQUE 
 
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE, 
    description TEXT

);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY, 
    logged_user INTEGER, 
    description TEXT, 
    project_name TEXT,
    client_name TEXT,
    summary TEXT,
    raised_date TIMESTAMP,
    due_date TIMESTAMP,
    status TEXT,
    tax_type INTEGER,
    discount FLOAT,
    comment TEXT,
    productprice FLOAT,
    product_amount INTEGER
 
);

CREATE TABLE invoiceitems (
    id SERIAL PRIMARY KEY, 
    description TEXT,
    price_per_unit FLOAT,
    amount INTEGER

);

CREATE TABLE taxtypes (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    percentage FLOAT,
    comment TEXT

);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY, 
    bank_name TEXT,
    bank_branch TEXT,
    invoice_id INTEGER,
    comment TEXT
  
);



