from flask import Flask,render_template,flash,request,redirect
from database_manager import *
from flask_session import Session
from additional import *

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
            redirect_add=f"/{role}/{idd}/home"
            return redirect(redirect_add)
    return render_template("login.html")

@app.route("/customer/<id>/home")
def login_customer(id):
    data=get_all_products()
    check=len(data)==1
    prof=extract_profile("customer",id)
    return render_template("customer.html",table_data=data,check=check,profile=prof)

@app.route("/supplier/<id>/home")
def login_supplier(id):
    prosold,revenue=supply_home(id)
    return render_template("supplier.html",prosold=prosold,revenue=revenue)

@app.route("/delivery_agent/<id>/home")
def login_delivery_agent(id):
    orcom=dagent_home(id)
    return render_template("delivery_agent.html",orcom=orcom)

@app.route("/supplier/<id>/management")
def supplier_management(id):
    data=get_supplier_product(id)
    empty=(len(data)==1)
    return render_template("supplier_management.html",table_data=data,check=empty)

@app.route("/supplier/<id>/management/add_product",methods=["GET","POST"])
def add_product(id):
    if request.method=="POST":
        name=request.form.get('name')
        price=float(request.form.get('price'))
        quantity=int(request.form.get('quantity'))
        material=request.form.get('material')
        desc=request.form.get('product_description')
        gender=request.form.getlist('gender')[0]

        mssg=validate_product_addition(name,price,quantity,material)
        if len(mssg):
            flash(mssg)
        else:
            add_supplier_product(id,name,price,quantity,material,desc,gender)
            flash("Product Added Successfully!")

    return render_template("add_product.html")

@app.route("/supplier/<id>/management/update_quantity",methods=["GET","POST"])
def update_quantity(id):
    if request.method=="POST":
        proid=int(request.form.get('name'))
        updqnty=int(request.form.get('price'))

        if check_seller(proid,id):
            seller_update_quantity(proid,updqnty)
            flash("Quantity Updated Successfully")
        else:
            flash("Invalid Product ID Entered")
    return render_template("update_quantity.html")

@app.route("/supplier/<id>/management/remove_product",methods=["POST","GET"])
def remove_product(id):
    if request.method=="POST":
        proid=int(request.form.get('name'))

        if check_seller(proid,id):
            delete_product(proid)
            flash("Product Deleted Successfully Successfully")
        else:
            flash("Invalid Product ID Entered")
    return render_template("remove_product.html")

@app.route("/supplier/<id>/pending_supplies")
def pending_supplies(id):
    data=get_supplier_product(id)
    empty=(len(data)==1)
    return render_template("pending_supplies.html",heading="Heading",heading_2="heading2",dialogue="Dialogue",table_data=data,check=empty)

@app.route("/supplier/<id>/delivered")
def supplier_delivered(id):
    data=get_supplier_product(id)
    empty=(len(data)==1)
    return render_template("supplier_items_delivered.html",heading="Heading",heading_2="heading2",dialogue="Dialogue",table_data=data,check=empty)

@app.route("/supplier/<id>/reviews")
def supplier_reviews(id):
    data=get_supplier_product(id)
    empty=(len(data)==1)
    return render_template("supplier_reviews.html",heading="Heading",heading_2="heading2",dialogue="Dialogue",table_data=data,check=empty)

@app.route("/supplier/<id>/account")
def supplier_profile(id):
    data=extract_profile("supplier",id)
    return render_template("supplier_profile.html",data=data)

@app.route("/customer/<id>/account")
def customer_profile(id):
    data=extract_profile("customer",id)
    return render_template("customer_profile.html",data=data)

@app.route("/customer/<id>/add_cart" ,methods = ["GET", "POST"])
def add_cart(id):
    if request.method=="POST":
        product_id=int(request.form.get('productid'))
        quantity=int(request.form.get('quantity'))
        mssg=validate_availability(product_id,quantity)
        if len(mssg):
            flash(mssg)
        else:
            check = check_cart(id,product_id)
            if(check):
                update_cart(id,product_id,quantity)
                flash("Updated Cart Successfully")
            else:
                add_to_cart(id,product_id,quantity)
                flash("Product Added Successfully!")
    return render_template("add_cart.html")
    
@app.route("/customer/<id>/remove_cart" ,methods = ["GET", "POST"])
def remove_cart(id):
    if request.method=="POST":
        product_id=int(request.form.get('name'))
        check = check_cart_remove(id,product_id)
        if(check):
            del_cart(id,product_id)
            flash("Product Removed from Cart Successfully")
        else:
            flash("Product Not Found In Cart")
    return render_template("remove_product.html")
    
@app.route("/customer/<id>/cart")
def view_cart(id):
    data =extract_cart(id)
    check=(len(data)==1)
    return render_template("view_cart.html", table_data = data,check=check)

@app.route("/customer/<id>/orders", methods=["GET", "POST"])
def view_orders(id):
    data =extract_orders(id)
    check=(len(data)==1)
    return render_template("view_orders.html", table_data = data,check=check)

@app.route("/customer/<id>/order", methods=["GET", "POST"])
def order_items(id):
    if request.method=="POST":
        address=request.form.get('address')
        pincode=request.form.get('pincode')
        mssg1=validate_address(id,address,pincode)
        mssg2 = validate_order(id)
        if len(mssg1):
            flash(mssg1)
        elif (len(mssg2)):
            flash(mssg2)
        else:
            add_order(id,address,pincode)
            flash("Order Placed Successfully!")
    return render_template("orders.html")
    
@app.route("/customer/<id>/review", methods=["GET", "POST"])
def add_review(id):
    if request.method=="POST":
        orderID=request.form.get('orderid')
        productID=request.form.get('productid')
        review = request.form.get('review')
        msg = validate_request(id, orderID , productID)
        if len(msg):
            flash(msg)
        else:
            add_reviews(id,orderID,productID,review)
            flash("Review Added Successfully!")
    return render_template("add_review.html")

@app.route("/customer/<id>/reviews" , methods = ["GET", "POST"])
def all_reviews(id):
    data = extract_reviews(id)
    check=(len(data)==1)
    return render_template("all_reviews.html", table_data = data,check=check)

@app.route("/delivery_agent/<id>/undelivered")
def undelivered_orders(id):
    data=get_undelivered_products(id)
    check=(len(data)==1)
    return render_template("undelivered_orders.html",table_data=data,check=check)

@app.route("/delivery_agent/<id>/delivered")
def delivered_orders(id):
    data=get_delivered_products(id)
    check=(len(data)==1)
    return render_template("delivered_orders.html",table_data=data,check=check)

@app.route("/delivery_agent/<id>/status")
def delivery_agent_status(id):
    status=get_delivery_status(id)
    return render_template("delivery_agent_status.html",status=status)

@app.route("/delivery_agent/<id>/change_status")
def change_status(id):
    change_delivery_status(id)
    return "Status Changed Successfully"

@app.route("/delivery_agent/<id>/account")
def delivery_agent_account(id):
    data=extract_profile("delivery_agent",id)
    return render_template("delivery_agent_profile.html",data=data)

@app.route("/delivery_agent/<id>/deliver",methods=["GET","POST"])
def deliver_product(id):
    if request.method=="POST":
        orderID=request.form.get('orderid')
        if check_order(id,orderID):
            deliver_order(orderID,id)
            flash("Order Delivered Successfully!")
        else:
            flash("Invalid Details Entered.")
    return render_template("deliver.html")

    
if __name__=="__main__":
    app.run(debug=True)