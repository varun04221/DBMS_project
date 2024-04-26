drop database everweave; 
CREATE DATABASE everweave;

USE everweave;

#admintable
CREATE TABLE IF NOT EXISTS admintable (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
INSERT INTO admintable VALUES (1, 'ABC');


#delivery_agent
CREATE TABLE IF NOT EXISTS delivery_agent (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(20) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    password varchar(20) not null,
    pincode varchar(6) not null,
    address varchar(255) not null, 
    PRIMARY KEY (ID)
);

#customers
CREATE TABLE IF NOT EXISTS customer (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email varchar(20) not null,
    phone VARCHAR(10) NOT NULL,
    password varchar(20) not null,
	pincode varchar(6) not null,
    address varchar(255) not null,
	orders_placed INT NOT NULL default 0,
    PRIMARY KEY (ID)
);

#supplier
CREATE TABLE IF NOT EXISTS supplier (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email varchar(20) not null,
    phone VARCHAR(10) NOT NULL,
    password varchar(20) not null,
	pincode varchar(6) not null,
    address varchar(255) not null,
    PRIMARY KEY (ID)
);

#product
CREATE TABLE IF NOT EXISTS product (
    productID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    supplierID INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    gender VARCHAR(15) NOT NULL,
    material VARCHAR(100) NOT NULL,
    product_description TEXT NOT NULL,
    CHECK (price > 0.00),
    CHECK (quantity >= 0),
    PRIMARY KEY (productID),
    FOREIGN KEY (supplierID) REFERENCES supplier(ID)
);

create table if not exists login(
	ID int not null auto_increment,
    role varchar(50) not null,
    usr_id int not null,
    primary key(ID)
);

CREATE TABLE IF NOT EXISTS cart (
	customerID INT NOT NULL, 
    productID INT NOT NULL,
    quantity INT NOT NULL,
    Foreign KEY(customerID) REFERENCES customer(ID),
	Foreign KEY(productID) REFERENCES product(productID)
);

	


CREATE TABLE IF NOT EXISTS orders(
	orderID INT NOT NULL auto_increment,
	customerID INT NOT NULL,
    pincode varchar(6) not null,
    address varchar(255) not null,
    primary key(orderID),
    Foreign KEY(customerID) REFERENCES customer(ID)
);

CREATE TABLE IF NOT EXISTS ORDER_desription(
	orderID INT NOT NULL,
	customerID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    Foreign KEY(customerID) REFERENCES customer(ID),
	Foreign KEY(productID) REFERENCES product(productID)	
);

CREATE TABLE IF NOT EXISTS cust_reviews(
	reviewId INT NOT NULL auto_increment,
    orderID INT NOT NULL,
	customerID INT NOT NULL,
    productID INT NOT NULL,
    review varchar(255) not null,
    primary key(reviewID),
    foreign key(orderID) references orders(orderID),
    Foreign KEY(customerID) REFERENCES customer(ID),
	Foreign KEY(productID) REFERENCES product(productID)	
);



-- insert into customer(name,email,password,orders_placed)
-- values('takla','takla@gmail','password',0);