DROP DATABASE IF EXISTS HikersHolidays;
CREATE DATABASE HikersHolidays;

USE HikersHolidays;

DROP TABLE IF EXISTS holidays;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS reservations;


CREATE TABLE holidays (
	Holiday_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Arrival_date DATE NOT NULL,
    Duration INT
);

CREATE TABLE customers (
    Customer_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Customer_fname VARCHAR(50) NOT NULL,
    Customer_lname VARCHAR(50) NOT NULL,
    Customer_email VARCHAR(100) NOT NULL,
    INDEX idx_customer_id (Customer_ID) 
);

 CREATE TABLE reservations (
    Reservation_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    RCustomer_ID INT NOT NULL, 
    RHoliday_ID INT NOT NULL,
    FOREIGN KEY (RCustomer_ID) REFERENCES customers(Customer_ID), 
    FOREIGN KEY (RHoliday_ID) REFERENCES holidays(Holiday_ID)
);


INSERT INTO holidays (Arrival_date, Duration)
VALUES
('2024-04-22', 3),
('2024-04-24', 7),
('2024-04-26', 3),
('2024-05-03', 3),
('2024-05-05', 7),
('2024-05-27', 3),
('2024-05-28', 7),
('2024-05-29', 14),
('2024-05-30', 3),
('2024-05-31', 7),
('2024-06-01', 14),
('2024-06-03', 3),
('2024-06-10', 3),
('2024-06-17', 3),
('2024-06-24', 3),
('2024-06-04', 7),
('2024-06-11', 7),
('2024-06-18', 7),
('2024-06-25', 7),
('2024-06-05', 14),
('2024-06-12', 14),
('2024-06-19', 14),
('2024-06-26', 14);


DROP PROCEDURE IF EXISTS add_customer;

DELIMITER //

CREATE PROCEDURE add_customer(
    IN fname VARCHAR(50),
    IN lname VARCHAR(50),
    IN email VARCHAR(100)
)
BEGIN
    -- Insert customer details into customers table
    INSERT INTO customers (Customer_fname, Customer_lname, Customer_email)
    VALUES (fname, lname, email);
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS add_reservation;

DELIMITER //

CREATE PROCEDURE add_reservation(
    IN customer_id INT,
    IN holiday_id INT
)
BEGIN
    -- Insert reservation for the customer
    INSERT INTO reservations (RCustomer_ID, RHoliday_ID)
    VALUES (customer_id, holiday_id);

END //

DELIMITER ;
