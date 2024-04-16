from flask import Flask,render_template,flash,request,redirect
from database_manager import validate_login,register
from flask_session import Session
from additional import validate

app = Flask(__name__)
app.secret_key='E09Yx_eEu1znZNPcg-XaR0FJH6ZbOjeK'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
Session(app)

@app.route("/",methods=["GET","POST"])
@app.route("/register",methods=["GET","POST"])
def register_page():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        pincode=request.form.get('pincode')
        address=request.form.get('address')
        confirm_password=request.form.get('confirm_password')
        register_as=request.form.getlist('register_as')[0]
        
        mssg=validate(name,email,password,confirm_password,register_as,phone,pincode,address)
        if len(mssg):
            flash(mssg)
        else:
            register(register_as,name,email,password,phone,address,pincode)
            flash("Registered Successfully!\n Please try logging in.")
    return render_template("register.html")



@app.route("/login",methods=["GET","POST"])
def login_page():

    if request.method=="POST":
        role=request.form.getlist("login_as")[0]
        email=request.form.get("email")
        password=request.form.get("password")

        idd=validate_login(role,email,password)
        if idd==0:
            flash("Invalid Login Details")
        else:
            redirect_add=f"/{role}/{idd}"
            return redirect(redirect_add)
    return render_template("login.html")

@app.route("/supplier")
def supplier():
    return render_template("supplier.html")

@app.route("/delivery")
def delivery():
    return render_template("delivery.html")


@app.route("/<role>/<id>")
def login_member(role,id):
    data=role;idd=id
    data,idd=idd,data
    return render_template(f"{role}.html")

if __name__=="__main__":
    app.run(debug=True)