CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    email TEXT,
    password TEXT,
    admin BOOLEAN

);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    phone TEXT,
    email TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users

 
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE,
    description TEXT,
    user_id INTEGER REFERENCES users
   

);


CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users ON DELETE CASCADE, 
    description TEXT, 
    project_id INTEGER REFERENCES projects ON DELETE CASCADE,
    client_id INTEGER REFERENCES clients ON DELETE CASCADE,
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
    id SERIAL PRIMARY KEY,
    invoice INTEGER REFERENCES invoices,
    user_id INTEGER REFERENCES users,
    name TEXT UNIQUE,
    description TEXT,
    price INTEGER
);


INSERT INTO  users (username, email, password, admin) VALUES ('admin123', 'admin@gmail.com', 'pbkdf2:sha256:260000$lyZYw1c6mQ50BHsl$7cb81fc63341a77a7b7846705ed9b8b1e07e1703cbb1c71b03df15bbe02944e5', True)




