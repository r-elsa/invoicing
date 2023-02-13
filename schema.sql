
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    email TEXT,
    password TEXT


);


CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE 
 
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE, 
    description TEXT

 
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY, 
    logged_user INTEGER, 
    description TEXT, 
    project_name TEXT,
    client_name TEXT,
    summary TEXT,
    raised_date DateTime,
    due_date DateTime,
    status TEXT,
    tax_type INTEGER,
    discount FLOAT,
    comment TEXT,
    productprice FLOAT,
    product_amount INTEGER,

 
);

CREATE TABLE IF NOT EXISTS invoiceitems (
    id SERIAL PRIMARY KEY, 
    description TEXT,
    price_per_unit FLOAT,
    amount INTEGER

);

CREATE TABLE IF NOT EXISTS taxtypes (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    percentage FLOAT,
    comment TEXT

);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY, 
    bank_name TEXT,
    bank_branch TEXT,
    invoice_id INTEGER,
    comment TEXT
  
);



