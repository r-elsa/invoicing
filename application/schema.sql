CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    email TEXT,
    password TEXT

);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL,
    name TEXT UNIQUE PRIMARY KEY,
    phone TEXT,
    email TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users

 
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL, 
    name TEXT UNIQUE PRIMARY KEY, 
    description TEXT,
    user_id INTEGER REFERENCES users

);

CREATE TABLE IF NOT EXISTS taxtypes (
    id SERIAL PRIMARY KEY, 
    tax_name TEXT,
    tax_percentage FLOAT,
    comment TEXT

);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY, 
    logged_user INTEGER REFERENCES users ON DELETE CASCADE, 
    description TEXT, 
    project_name TEXT REFERENCES projects ON DELETE CASCADE,
    client_name TEXT REFERENCES clients ON DELETE CASCADE,
    summary TEXT,
    raised_date TIMESTAMP,
    due_date TIMESTAMP,
    status TEXT,
    tax_type INTEGER,
    discount FLOAT,
    comment TEXT,
    product_amount INTEGER,
    final_price FLOAT

 
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL, 
    invoice INTEGER REFERENCES invoices,
    user_id INTEGER REFERENCES users,
    name TEXT UNIQUE PRIMARY KEY,
    description TEXT,
    price INTEGER
);







