from database_manager import email_already_registered

def validate(name,email,password1,password2,role):
    error=""
    if len(name)>=50:
        error+="Name should be less than 50 characters\n"
    if password1!=password2:
        error+="Passwords do not match\n"
    if email_already_registered(role,email):
        error+="This email is already registered. Try logging in.\n"
    return error