import mysql.connector
from random import randint

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
    
def extract_cart(id):
    database = connect_database()
    try:
        cursor=database.cursor()
        data=[["Product ID","Product Name","Supplier ID","Price","Gender","Material","Description","Quantity"]]
        cursor.execute(f"SELECT p.productID, p.name, p.supplierID, p.price, p.gender, p.material, p.product_description,od.quantity AS order_quantity FROM cart od INNER JOIN product p ON od.productID = p.productID WHERE od.customerID = {id};")
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data


def extract_reviews(id):
    database = connect_database()
    try:
        data=[["ReviewID","OrderID","CustomerID","ProductID","Review"]]
        cursor=database.cursor()
        cursor.execute(f"select * from cust_reviews where customerID={id}")
        data+=cursor.fetchall()
        # print(data)
    finally:
        cursor.close()
        database.close()
    return data
    

def extract_orders(id):
    database = connect_database()
    try:
        cursor=database.cursor()
        data=[["Order ID","Product ID","Product Name","Supplier ID","Price","Gender","Material","Description","Quantity"]]
        cursor.execute(f"SELECT od.orderID, p.productID, p.name, p.supplierID, p.price, p.gender, p.material, p.product_description,od.quantity AS order_quantity FROM order_desription od INNER JOIN product p ON od.productID = p.productID WHERE od.orderID = {id};")
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data

def not_exist_order(id, orderid, productid):
    database = connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from ORDER_desription where customerID={id} and orderID={orderid} and productID={productid}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)==0
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
        
def product_not_availaible(product_id,quantity):
    database=connect_database()
    try:
        
        cursor=database.cursor()
        product = "product"
        cursor.execute(f"select * from {product} where quantity<{quantity} and productID={product_id}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)>0

def check_cart(id,product_id):
    set=0
    database=connect_database()
    try:
        cursor=database.cursor()
        cart = "cart"
        cursor.execute(f"select * from {cart} where customerID={id} and productID={product_id}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    if len(data)>0: set=1
    return set

def check_cart_remove(id,product_id):
    set=0
    database=connect_database()
    try:
        cursor=database.cursor()
        cart = "cart"
        cursor.execute(f"select * from {cart} where customerID={id} and productID={product_id}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    if len(data)>0: set=1
    return set

def add_to_cart(id,product_id,quantity):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"insert into cart(customerID,productID, quantity) values({id},{product_id},{quantity})")
        database.commit()
    finally:
        cursor.close()
        database.close()

def update_cart(id,product_id,quantity):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"SELECT quantity FROM cart where customerID = {id} and productID = {product_id}")
        data = cursor.fetchall()
        quantity+= int(data[0][0])
        cursor.execute(f"update cart set quantity = {quantity} where customerID={id} and productID={product_id}")
        database.commit()
    finally:
        cursor.close()
        database.close()

def del_cart(id, product_id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"delete from cart where customerID={id} and productID={product_id}")
        database.commit()
    finally:
        cursor.close()
        database.close()
        
def address_not_added(id,address,pincode):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from customer where ID = {id} and address='{address}' and pincode={int(pincode)}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)==0
    
def orders_check(id):
    database=connect_database()
    error=""
    set=0
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from cart where customerID = {id}")
        data=cursor.fetchall()
        for i in range(len(data)):
            cursor.execute(f"select quantity from product where productID = {data[i][1]}")
            compare = cursor.fetchall()
            if(data[i][2] > compare[0][0]):
                set=1
                error+="Product ID: "+str(data[i][1])+" is out of stock\n"
            else:
                set =1 
            
            # data[i]+=cursor.fetchall()[0]
    finally:
        if (set == 0):
            error += "Cart is empty"
        cursor.close()
        database.close()
    return error

def revenue_sup(id,quantity,price):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"update supplier set products_sold=products_sold+{quantity} where ID={id}")
        database.commit()
        cursor.execute(f"update supplier set revenue=revenue+{quantity*price} where ID={id}")
        database.commit()
    finally:
        cursor.close()
        database.close()
    
def add_order(id,address,pincode):
    database= connect_database()
    try:
        cursor = database.cursor()
        cursor.execute(f"insert into orders(customerID,address,pincode,delID) values({id},'{pincode}','{address}',{delivery_agent_avlbl()})")
        database.commit()
        cursor.execute(f"select orderID from orders where customerID = {id}")
        data1 = cursor.fetchall()
        order_id = data1[len(data1)-1][0]
        cursor.execute(f"select * from cart where customerID={id}")
        data=cursor.fetchall()
        cart_values=extract_cart(id)
        for ele in cart_values[1:]:
            revenue_sup(ele[2],ele[7],ele[3])
        for i in range(len(data)):
            cursor.execute(f"insert into ORDER_desription(orderID,customerID,productID,quantity) values({order_id},{id},{data[i][1]},{data[i][2]})")
            database.commit()
            cursor.execute(f"update product set quantity=quantity-{data[i][2]} where productID={data[i][1]}")
            database.commit()
        cursor.execute(f"delete from cart where customerID={id}")
        database.commit()
    finally:
        cursor.close()
        database.close()

def add_reviews(id, orderid, productid,reviews):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"insert into cust_reviews(orderID,customerID,productID, review) values({orderid},{id},{productid},'{reviews}')")
        database.commit()
    finally:
        cursor.close()
        database.close()

def get_undelivered_products(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from orders where delID={id} and delivery_status={False}")
        data=[["OrderID","CustomerID","Pincode","Address","Delivery status","Delivery Agent ID"]]
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data

def get_delivered_products(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from orders where delID={id} and delivery_status={True}")
        data=[["OrderID","CustomerID","Pincode","Address","Delivery status","Delivery Agent ID"]]
        data+=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return data

def get_delivery_status(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select active_status from delivery_agent where ID={id}")
        data=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data[0]

def change_delivery_status(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"update delivery_agent set active_status=NOT active_status where ID={id}")
        database.commit()
    finally:
        cursor.close()
        database.close()

def delivery_agent_avlbl():
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select ID from delivery_agent where active_status=true")
        data=cursor.fetchall()
        if len(data):
            data=data[randint(0,len(data)-1)][0]
        else:
            data=-1
    finally:
        cursor.close()
        database.close()
    return data

def check_order(delid,orderid):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select * from orders where delID={delid} and orderID={orderid}")
        data=cursor.fetchall()
    finally:
        cursor.close()
        database.close()
    return len(data)

def deliver_order(orderid,delid):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"update orders set delivery_status=true where orderID={orderid}")
        database.commit()
        cursor.execute(f"update delivery_agent set orders_delivered=orders_delivered+1 where ID={delid}")
        database.commit()
    finally:
        cursor.close()
        database.close()

def dagent_home(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select orders_delivered from delivery_agent where ID={id}")
        data=cursor.fetchall()[0][0]
    finally:
        cursor.close()
        database.close()
    return data

def supply_home(id):
    database=connect_database()
    try:
        cursor=database.cursor()
        cursor.execute(f"select products_sold,revenue from supplier where ID={id}")
        data=cursor.fetchall()[0]
    finally:
        cursor.close()
        database.close()
    return data[0],data[1]
    
    
    
    
if __name__=="__main__":
    # print(extract_profile('supplier',1))
    #print(get_supplier_product(1))
    #print(check_seller(1,5))
    print(dagent_home(1))
    print(supply_home(1))