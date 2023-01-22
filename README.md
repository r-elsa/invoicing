# Invoicing application

## Requirements specification

### Purpose of the application

The application helps users to keep track of their invoices in the CRUD method (create, read, update and delete invoices). The application can be used by several users.

### Users

The application has regular users and administrators. _regularusers_ can only keep track of their own invoices. An  _adminuser_ has greater rights.

### UI draft

The application consists of four different views.

The application opens to the login view. Upon successful login, the application switches to the user's dashboard. From the dashboard the user can view, create new, update existing and and delete invoices.

### Functionality offered by the basic version

#### Before logging in

- The user can create a user id by giving a unique username, their email address and a password that is at least 7 characters long. 
- The user cab log in to the application by entering their username and password.
- If the user does not exist, or the password does not match, the system will notify.

#### After logging in

- The user can see their created invoices in the dashboard.
- The user can create new invoices.
- The user can view existing invoices in more detail.
- The user can update existing invoices.
- The user can delete an invoice and the invoice isappears from the dashboard.
- The user can log out of the system.

### Further development ideas

If time permits, the following functionalities will be added (not in order).
- possibility to mark invoices as Created, Sent and Paid.
- create ready products and services to add to the invoice
- print invoice
- email invoice
- add customers
- more functionality for invoice e.g.personal message
- user can not create many account with same email address
