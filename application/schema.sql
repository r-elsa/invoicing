CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    email TEXT,
    password TEXT,
    admin BOOLEAN

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


INSERT INTO  users (username, email, password, admin) VALUES ('admin123', 'admin@gmail.com', 'pbkdf2:sha256:260000$lyZYw1c6mQ50BHsl$7cb81fc63341a77a7b7846705ed9b8b1e07e1703cbb1c71b03df15bbe02944e5', True)




