import mysql.connector

def connect_database():
    database=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
    )
    return database

def disconnect_database(database):
    database.close()

def validate_login(role,email,password):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute("use everweave")
        cursor.execute(f"select ID from {role} where email='{email}' and password='{password}'")
        data=cursor.fetchall()
        if len(data)==0:
            data=0
        else:
            data=data[0][0]
    finally:
        disconnect_database(database)
    return data

def register(role,name,email,password):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute("use everweave")
        cursor.execute(f"insert into {role}(name,email,password) values('{name}','{email}','{password}')")
        database.commit()
    finally:
        disconnect_database(database)

def email_already_registered(role,email):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute("use everweave")
        cursor.execute(f"select * from {role} where email='{email}'")
        data=cursor.fetchall()
    finally:
        disconnect_database(database)
    return len(data)>0


if __name__=="__main__":
    print(validate_login('Customer','takla@gmail','password'))
    #register('customer','takla','jingle@ajd','password')
    print(validate_login('customer','jingle@ajd','password'))
    database=connect_database()
    cursor=database.cursor()
    cursor.execute("use everweave")
    cursor.execute("select * from customer")
    data=cursor.fetchall()
    print(data)
    disconnect_database(database)