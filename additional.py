from database_manager import email_already_registered , product_not_availaible, address_not_added, orders_check, not_exist_order

def validate(name,email,password1,password2,role,phone,pincode,address):
    error=""
    if len(name)>=50:
        error+="Name should be less than 50 characters\n"
    if password1!=password2:
        error+="Passwords do not match\n"
    if email_already_registered(role,email):
        error+="This email is already registered. Try logging in.\n"
    if len(phone)!=10:
        error+="Phone number should be of length 10\n"
    if len(pincode)!=6:
        error+="Pincode should be of length 6\n"
    if len(address)>256:
        error+="Address should not exceed 256 characters\n"
    return error

def validate_product_addition(name,price,quantity,material):
    error=""
    if len(name)>50:
        error+="Product name is too long.\n"
    if price<=0:
        error+="Invalid Price.\n"
    if quantity<=0 or int(quantity)!=quantity:
        error+="Invalid Quantity.\n"
    if len(material)>100:
        error+="Product material name is too long.\n"
    return error

def validate_availability(product_id,quantity):
    error=""
    if product_not_availaible(product_id,quantity):
        error+="Product is not available.\n"
    return error

def validate_address(id,address,pincode):
    error=""
    if len(address)>256:
        error+="Address should not exceed 256 characters\n"
    if len(pincode)!=6:
        error+="Pincode should be of length 6\n"
    if address_not_added(id,address,pincode):
        error+="Not a verified address"
    return error

def validate_order(id):
    error= orders_check(id)
    return error

def validate_request(id,orderid,productid):
    error=""
    if not_exist_order(id,orderid,productid):
        error+="Cannot take review of product because user has not ordered it before"
    return error
    

