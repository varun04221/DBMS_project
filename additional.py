from database_manager import email_already_registered

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