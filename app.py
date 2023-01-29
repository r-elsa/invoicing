from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("login.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form["username"]
    password = request.form["password"]
    return render_template("dashboard.html", username=username, password=password)

@app.route("/dashboard/create", methods=["POST"])
def create():
    invoice_number = request.form["invoice"]
    taxvalue = request.form.getlist("taxvalue")
    message = request.form["message"]
    return render_template("invoice.html", invoice_number = invoice_number,
                                            taxvalue=taxvalue,
                                            message=message
    )



@app.route("/dashboard/invoice/<int:id>")
def page3(id):
    return "This is invoice number " + str(id)




