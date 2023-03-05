# Invoicing application


## To start application

1) create database and ensure that postgres is running (e.g. "sudo service postgresql start" on linux) 
2) write database address and secret key to .env file
3) install poetry if you don't already have it installed already. I acknowledge that poetry is not part of the course material, yet a useful technology.
    https://ohjelmistotekniikka-hy.github.io/python/viikko2#poetry-ja-riippuvuuksien-hallinta
3) >poetry install
4) >poetry shell (inside project folder /application)
5) create tables (e.g. "sudo -u <user> -d nameofdatabase -f schema.sql -p port" on linux)
6) >poetry run flask --debug run


## Final submission status update:
- The application does take into account CSRF.
- The user can delete an invoice.
- The user can update the status of an invoice.
- The application has functionality of extended filtering based on product or client.
- The application has an admin, which can be tested by logging in with the following credentials:  username "admin123" and password "adminpwd".



## Välipalautus 3 status update:
- The application does not use ORM -techniques anymore, as per request. 
- The application is now divided to different files -  app, db and routes. 
- The application does now use 5 tables - users, invoices, clients, projects and products. 
- The UI is improved for the dashboard. 
- The application does not yet take into account XSS and CSRF.
- The user can not yet modify and/or delete an invoice or sort invoices based on parameters.
- Currently it is only possible to add one product to an invoice, this will be improved to the next due date. 



## Välipalautus 2 status update:
- The application has a login and signup form.
- The user can create an invoice and it is displayed on the users dashboard.
- The user can log out of the application.
- The application does not yet count the total amount of the invoice/invoices.
- The application does not yet take into account XSS and CSRF.
- The application does not yet use all of the intended tables in the database.
- The user can not yet make changes and/or delete and invoice or sort invoices based on parameters.



## Requirements specification

### Purpose of the application

The application helps users to keep track of their invoices in the CRUD method (create, read, update and delete invoices) and some filtering functionality. The application can be used by several regular users and has an admin user.

### Users

The application has regular users and administrators. _regularusers_ can only keep track of their own invoices. An  _adminuser_ has greater rights in terms of viewing, updating and deleting  invoices of regular users.

### UI draft

The application consists of 8 different views.

The application opens to the login view. Upon successful login, the application switches to the user's dashboard. If the user has not signed up yet, the user can choose to sign up and is upon successful signup given the dashboard view. From the dashboard the user can view, create new, update existing and delete invoices. In order to create an invoice the user has to create a client, a project and a product, which all have separate views. The user can also filter invoices based on project or client.

### Functionality offered for regular user (user)

- The user can create a user id by giving a unique username, their email address and a password that is at least 7 characters long. 
- The user can log in to the application by entering their username and password.
- If the user does not exist, or the password does not match, the system will notify.
- The user can add a new project, client and product.
- The user can create a new invoice and see their created invoice in the dashboard.
- The user can update the status of an existing invoice.
- The user can delete an invoice and the invoice disappears from the dashboard.
- The user can filter their invoices based on client and project.
- The user can log out of the system.

### Functionality offered for admin user (admin)
- The admin can log in using the username "admin123" and password "adminpwd".
- The admin can see created invoices of all _regularusers_ in the dashboard.
- The admin can update and delete invoices created by all _regularusers_.
- The admin can add new projects, clients and products and create new invoices.
- The admin can NOT filter based on client and project.
- The admin can log out of the system.
