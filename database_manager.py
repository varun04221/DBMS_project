import mysql.connector

def connect_database():
    database=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="everweave"
    )
    return database


def validate_login(role,email,password):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select ID from {role} where email='{email}' and password='{password}'")
        data=cursor.fetchall()
        if len(data)==0:
            data=0
        else:
            data=data[0][0]
    finally:
        cursor.close()
        database.close()
    return data

def register(role,name,email,password,phone,address,pincode):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"insert into {role}(name,email,password,phone,address,pincode) values('{name}','{email}','{password}','{phone}','{address}','{pincode}')")
        database.commit()
    finally:
        cursor.close()
        database.close()

def email_already_registered(role,email):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from {role} where email='{email}'")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)>0

def extract_profile(role,id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from {role} where ID='{id}'")
        data=cursor.fetchall()[0]
        data=[data[0],data[1],data[2],data[3],data[5],data[6]]
    finally:
        cursor.close()
        database.close()
    return data

def customer_reviews(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from delivery_agent_review where cust_ID='{id}'")
        data=cursor.fetchall()[0]
        cursor.execute(f"select * from supplier_review where cust_ID='{id}'")
        data+=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data

def delivery_agent_reviews(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from delivery_agent_review where del_ID='{id}'")
        data=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data

def supplier_review(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from supplier_review where sup_ID='{id}'")
        data=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data

def customer_orders(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from order_history where cust_ID='{id}'")
        data=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data

def get_supplier_product(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        data=[["Product ID","Name","Supplier ID","Price","Quantity","Gender","Material","Product_Description"]]
        cursor.execute(f"select * from product where supplierID='{id}'")
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data

def get_all_products():
    database=connect_database()
    try:
        cursor=database.cursor()
        data=[["Product ID","Name","Supplier ID","Price","Quantity","Gender","Material","Product_Description"]]
        cursor.execute(f"select * from product")
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data
    

def add_supplier_product(id,name,price,quantity,material,desc,gender):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"insert into product(name,supplierID,price,quantity,gender,material,product_description) values('{name}','{id}','{price}','{quantity}','{gender}','{material}','{desc}')")
        database.commit()
    finally:
        cursor.close()
        database.close()

def check_seller(pro_id,seller_id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select productID from product where supplierID={seller_id} and productID={pro_id}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)==1

def seller_update_quantity(pro_id,upd_quantity):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"update product set quantity={upd_quantity} where productID={pro_id}")
        database.commit()
    finally:
        cursor.close()
        database.close()

def delete_product(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"delete from product where productID={id}")
        database.commit()
    finally:
        cursor.close()
        database.close()

if __name__=="__main__":
    print(extract_profile('supplier',1))
    #print(get_supplier_product(1))
    print(check_seller(1,5))