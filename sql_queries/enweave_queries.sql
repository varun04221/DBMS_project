drop database everweave;

CREATE DATABASE everweave;

USE everweave;

#admintable
CREATE TABLE IF NOT EXISTS admintable (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
INSERT INTO admintable VALUES (1, 'ABC');

#cust_address
CREATE TABLE IF NOT EXISTS customer_addr (
    ID INT NOT NULL,
    pincode VARCHAR(15) NOT NULL,
    full_addr VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID) REFERENCES customers(ID)
);

#agent_address
CREATE TABLE IF NOT EXISTS agent_addr(
    ID INT NOT NULL,
    pincode VARCHAR(15) NOT NULL,
    full_addr VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID) REFERENCES delivery_agent(ID)
);


#supplier_address
CREATE TABLE IF NOT EXISTS supplier_addr(
    ID INT NOT NULL,
    pincode VARCHAR(15) NOT NULL,
    full_addr VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID) REFERENCES supplier(ID)
);

#delivery_agent
CREATE TABLE IF NOT EXISTS delivery_agent (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    deli_review VARCHAR(50),
    del_agent_avai VARCHAR(10) NOT NULL,
    email VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID)
);

#address
CREATE TABLE IF NOT EXISTS address (
    ID INT NOT NULL AUTO_INCREMENT,
    customer_ID INT NOT NULL,
    order_no INT NOT NULL,
    pincode VARCHAR(15) NOT NULL,
    full_addr VARCHAR(255) NOT NULL,
    PRIMARY KEY (ID)
);



#customers
CREATE TABLE IF NOT EXISTS customers (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    coupons INT NOT NULL,
    orders_ID INT NOT NULL,
    email VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID)
);




#coupons
CREATE TABLE IF NOT EXISTS coupons(
    ID INT NOT NULL,
    cust_ID INT NOT NULL, 
    discount_percentage DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (ID),
    FOREIGN KEY (cust_ID) REFERENCES customers(ID)
);

#payments
CREATE TABLE IF NOT EXISTS Payments (
    ID INT NOT NULL AUTO_INCREMENT,
    paymentMethod VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2)  NOT NULL DEFAULT 0.00,
    paymentStatus VARCHAR(10),
    cust_ID INT NOT NULL, 
    ord_ID INT NOT NULL,
    PRIMARY KEY (ID,paymentMethod),
    FOREIGN KEY (cust_ID) REFERENCES customers(ID)
);


#supplier
CREATE TABLE IF NOT EXISTS supplier (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (address_ID) REFERENCES address(ID),
);

#product
CREATE TABLE IF NOT EXISTS product (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    supplierID INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    gender VARCHAR(100) NOT NULL,
    material VARCHAR(100) NOT NULL,
    avail_status VARCHAR(100) NOT NULL,
    product_description TEXT NOT NULL,
    CHECK (price > 0.00),
    CHECK (quantity >= 0),
    PRIMARY KEY (ID),
    FOREIGN KEY (supplierID) REFERENCES supplier(ID)
);

#product_review
CREATE TABLE IF NOT EXISTS product_review (
    cust_ID INT NOT NULL,
    ord_ID INT NOT NULL,
    productID INT NOT NULL,
    rating INT NOT NULL,
    line_review TEXT,
    review_date DATE NOT NULL,
    CHECK (rating >= 1 AND rating <= 5),
    PRIMARY KEY (cust_ID, productID), 
    FOREIGN KEY (cust_ID) REFERENCES customers(ID),
	FOREIGN KEY (productID) REFERENCES product(ID)
);

#order history
CREATE TABLE IF NOT EXISTS order_history (
    order_ID INT NOT NULL,
    cust_ID INT NOT NULL,
    da_ID INT NOT NULL,
    product_ID INT NOT NULL,
    supp_ID INT NOT NULL,
    del_ID INT NOT NULL,
    orders_placed INT NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    
    PRIMARY KEY (order_ID, cust_ID),

    FOREIGN KEY (cust_ID) REFERENCES customers(ID),
    FOREIGN KEY (da_ID) REFERENCES delivery_agent(ID),
    FOREIGN KEY (product_ID) REFERENCES product(ID),
    FOREIGN KEY (supp_ID) REFERENCES supplier(ID)
);


#cart
CREATE TABLE IF NOT EXISTS cart (
    cust_ID INT NOT NULL,
    productID INT NOT NULL,
    order_ID INT NOT NULL,
    PRIMARY KEY (cust_ID, order_ID),
    FOREIGN KEY (cust_ID) REFERENCES customers(ID),
    FOREIGN KEY (productID) REFERENCES product(ID)
);

ALTER TABLE address
ADD CONSTRAINT fk_customer_ID
FOREIGN KEY (customer_ID) REFERENCES customers(ID);


-- INSERT INTO delivery_agent (name, phone, deli_review, del_agent_avai) VALUES
-- ('John Doe', '1234567890', 'Excellent service!', 'yes'),
-- ('Alice Smith', '9876543210', 'Great communication skills.', 'no'),
-- ('Bob Johnson', '5554443333', 'Fast delivery.', 'yes'),
-- ('Emma Lee', '1112223333', 'Friendly and efficient.', 'yes'),
-- ('Michael Brown', '9998887777', 'Professional demeanor.', 'no'),
-- ('Samantha Wilson', '4445556666', 'Polite and courteous.', 'yes'),
-- ('David Jones', '7778889999', 'Good overall experience.', 'no'),
-- ('Jennifer Martinez', '3332221111', 'Prompt and reliable.', 'yes'),
-- ('Daniel Davis', '6667778888', 'Helpful and attentive.', 'yes'),
-- ('Jessica Taylor', '2223334444', 'Knowledgeable about routes.', 'no');

-- show tables;

-- select * from delivery_agent;

-- INSERT INTO customers (name, phone, address_ID, coupons, orders_ID) VALUES
-- ('John Doe', '1234567890', 1, 0, 1001),
-- ('Alice Smith', '9876543210', 2, 1, 1002),
-- ('Bob Johnson', '5554443333', 3, 2, 1003),
-- ('Emma Lee', '1112223333', 4, 0, 1004),
-- ('Michael Brown', '9998887777', 5, 1, 1005),
-- ('Samantha Wilson', '4445556666', 6, 0, 1006),
-- ('David Jones', '7778889999', 7, 2, 1007),
-- ('Jennifer Martinez', '3332221111', 8, 1, 1008),
-- ('Daniel Davis', '6667778888', 9, 0, 1009),
-- ('Jessica Taylor', '2223334444', 10, 3, 1010);
-- select * from customers;

-- INSERT INTO address (customer_ID, order_no, pincode, full_addr) VALUES
-- (1, 1, '12345', '123 Main Street'),
-- (2, 1, '54321', '456 Elm Street'),
-- (3, 1, '98765', '789 Oak Street'),
-- (4, 1, '67890', '321 Pine Street'),
-- (5, 1, '13579', '654 Maple Street'),
-- (6, 1, '24680', '987 Cedar Street'),
-- (7, 1, '10101', '135 Walnut Street'),
-- (8, 1, '20202', '246 Cherry Street'),
-- (9, 1, '30303', '357 Birch Street'),
-- (10, 1, '40404', '468 Spruce Street');

-- select * from address;


-- INSERT INTO coupons (coupon_ID, cust_ID, discount_percentage) VALUES
-- (1, 1, 10.50),
-- (2, 2, 15.25),
-- (3, 3, 20.00),
-- (4, 4, 25.75),
-- (5, 5, 30.00),
-- (6, 6, 35.50),
-- (7, 7, 40.25),
-- (8, 8, 45.00),
-- (9, 9, 50.75),
-- (10, 10, 55.00);
-- select * from coupons;


-- INSERT INTO Payments (paymentMethod, amount, paymentStatus, cust_ID, ord_ID) VALUES
-- ('Credit Card', 2005.50, 'Pending', 1, 1001),
-- ('UPI', 4545.75, 'Completed', 2, 1002),
-- ('Debit Card', 342.20, 'Completed', 3, 1003),
-- ('Netbanking', 5500.00, 'Pending', 4, 1004),
-- ('Bank Transfer', 75000.90, 'Pending', 5, 1005),
-- ('Credit Card', 15562.35, 'Completed', 6, 1006),
-- ('UPI', 30129.99, 'Completed', 7, 1007),
-- ('Debit Card', 44879.80, 'Pending', 8, 1008),
-- ('Cash', 21218.75, 'Pending', 9, 1009),
-- ('Bank Transfer', 1483.20, 'Completed', 10, 1010);

-- select * from Payments;


-- INSERT INTO supplier (name, address_ID) VALUES
-- ('Supplier1', 1),
-- ('Supplier2', 2),
-- ('Supplier3', 3),
-- ('Supplier4', 4),
-- ('Supplier5', 5),
-- ('Supplier6', 6),
-- ('Supplier7', 7),
-- ('Supplier8', 8),
-- ('Supplier9', 9),
-- ('Supplier10', 10);

-- select * from supplier;


-- INSERT INTO product (name, supplierID, price, quantity, gender, material, avail_status, product_description) VALUES
-- ('Organic Cotton T-Shirt', 1, 129.99, 50, 'Unisex', 'Organic Cotton', 'In Stock', 'A comfortable and eco-friendly t-shirt made from organic cotton.'),
-- ('Linen Shirt', 2, 245.75, 30, 'Male', 'Linen', 'In Stock', 'A stylish and breathable shirt made from natural linen fibers.'),
-- ('Hemp Jeans', 3, 365.00, 20, 'Male', 'Hemp', 'In Stock', 'Durable and sustainable jeans crafted from hemp fibers.'),
-- ('Bamboo Dress', 4, 545.99, 40, 'Female', 'Bamboo', 'In Stock', 'A luxurious dress made from soft and sustainable bamboo fabric.'),
-- ('Wool Sweater', 5, 579.99, 15, 'Unisex', 'Wool', 'In Stock', 'Stay warm and cozy with this wool sweater, sourced from ethically raised sheep.'),
-- ('Silk Scarf', 6, 649.00, 10, NULL, 'Silk', 'In Stock', 'Add elegance to your outfit with this luxurious silk scarf.'),
-- ('Organic Cotton Hoodie', 7, 69.95, 25, 'Unisex', 'Organic Cotton', 'In Stock', 'A stylish and eco-friendly hoodie made from organic cotton.'),
-- ('Linen Shorts', 8, 359.50, 35, 'Female', 'Linen', 'In Stock', 'Stay cool and comfortable in these breathable linen shorts.'),
-- ('Alpaca Wool Sweater', 9, 99.99, 50, 'Unisex', 'Alpaca Wool', 'In Stock', 'Experience unmatched softness and warmth with this alpaca wool sweater.'),
-- ('Hemp Backpack', 10, 5109.00, 8, NULL, 'Hemp', 'In Stock', 'A durable and sustainable backpack made from hemp fibers.');

-- select * from product;


-- INSERT INTO product_review (cust_ID, ord_ID, productID, rating, line_review, review_date) VALUES
-- (1, 201, 1, 5, 'The organic cotton t-shirt is incredibly soft and fits perfectly. Will definitely buy again!', '2024-01-15'),
-- (2, 202, 4, 4, 'Love the hemp jeans! They are sturdy and comfortable. Great sustainable option.', '2024-01-17'),
-- (3, 203, 7, 5, 'These linen shorts are fantastic! They are breathable and look great.', '2024-01-20'),
-- (4, 204, 8, 3, 'The watch is stylish, but I expected better quality for the price.', '2024-01-22'),
-- (5, 205, 10, 5, 'The alpaca wool sweater is amazing! It is so soft and warm. Highly recommend it.', '2024-01-25'),
-- (6, 206, 2, 4, "The bamboo dress is elegant and comfortable. Received many compliments!", '2024-01-28'),
-- (7, 207, 5, 5, 'I am thrilled with my purchase of the wool sweater. Its cozy and well-made.', '2024-02-01'),
-- (8, 208, 3, 4, 'The hemp backpack is durable and spacious. Perfect for everyday use.', '2024-02-04'),
-- (9, 209, 6, 5, 'The organic cotton hoodie is super soft and feels great on the skin. Love it!', '2024-02-07'),
-- (10, 210, 9, 4, 'The silk scarf is beautiful and adds a touch of luxury to any outfit. Very pleased with my purchase.', '2024-02-09');

-- select * from product_review;



-- INSERT INTO order_history (order_ID, cust_ID, da_ID, product_ID, supp_ID, del_ID, orders_placed, order_date, delivery_date)
-- VALUES
-- (1, 1, 1, 1, 1, 1, 2, '2024-01-01', '2024-01-03'),
-- (2, 2, 2, 2, 2, 2, 1, '2024-01-02', '2024-01-04'),
-- (3, 3, 3, 3, 3, 3, 3, '2024-01-03', '2024-01-05'),
-- (4, 4, 4, 4, 4, 4, 1, '2024-01-04', '2024-01-06'),
-- (5, 5, 5, 5, 5, 5, 2, '2024-01-05', '2024-01-07'),
-- (6, 6, 6, 6, 6, 6, 1, '2024-01-06', '2024-01-08'),
-- (7, 7, 7, 7, 7, 7, 2, '2024-01-07', '2024-01-09'),
-- (8, 8, 8, 8, 8, 8, 3, '2024-01-08', '2024-01-10'),
-- (9, 9, 9, 9, 9, 9, 1, '2024-01-09', '2024-01-11'),
-- (10, 10, 10, 10, 10, 10, 2, '2024-01-10', '2024-01-12');

-- select * from order_history;


-- INSERT INTO cart (cust_ID, productID, order_ID) VALUES
-- (1, 1, 201),
-- (2, 2, 202),
-- (3, 3, 203),
-- (4, 4, 204),
-- (5, 5, 205),
-- (6, 6, 206),
-- (7, 7, 207),
-- (8, 8, 208),
-- (9, 9, 209),
-- (10, 10, 210);

-- select * from cart;
