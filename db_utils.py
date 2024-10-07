import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


class DbOperationError(Exception):
    pass


# information needed to connect to database
def _connect_to_db(db_name):
    cnx = None  # Initialize to None
    try:
        cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
        )
        return cnx
    except Exception as e:
        raise DbConnectionError("Failed to connect to DB: {}".format(e))
    # error message if failing to connect to database


def format_date(date):
    return date.strftime("%d-%m-%Y")


# This function shows the user all available holiday dates and durations
def get_holiday_dates():
   
    db_connection = None
    holidays = []
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)   # connection to database
        cur = db_connection.cursor()
        print(f"Connected to database: {db_name}")

        query = """SELECT Holiday_ID, Arrival_date, Duration FROM holidays"""   # query ran in mysql to select data
        cur.execute(query)
        result = cur.fetchall()
      
        for Holiday_ID, date, duration in result:
            formatted_date = date.strftime("%Y-%m-%d")  # Format the date as "YYYY-MM-DD"
            holiday_date_object = {
                "holiday_id": Holiday_ID,
                "arrival_date": formatted_date,
                "duration": duration
            }
            holidays.append(holiday_date_object)    # holiday dates appended to holidays list as dicitonary

        cur.close()

    # if connection to database has failed
    except Exception:
        raise DbConnectionError("Failed to read data :( please try again")

    finally:
        if db_connection:
            db_connection.close()  # once query is ran the connection to the dataase is closed
    return holidays


# this function creates a reservation and inputs record into database using the stored procedure

def create_reservation(customer_id, holiday_id):
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database: {db_name}")

        query = """CALL add_reservation (%s, %s)"""  # Assuming add_reservation is a stored procedure
        cur.execute(query, (customer_id, holiday_id))
        # Assuming add_reservation returns the reservation ID as the last inserted ID
        reservation_id = cur.lastrowid

        db_connection.commit()

        new_reservation = {
            "reservation_id": reservation_id,
            "holiday_id": holiday_id,
            "customer_id": customer_id
        }

        return new_reservation
    
    # if reservation entry has failed
    except Exception as e:
        raise DbConnectionError("Failed to execute query: {}".format(e))

    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")


# this function selects customers that are already in the database
def get_customers():
    customers = []
    db_connection = None
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT Customer_ID,Customer_fname,Customer_lname,Customer_email  FROM customers"""

        cur.execute(query)

        result = cur.fetchall()  # this is a list with db records where each record is a tuple
        for Customer_ID, Customer_fname, Customer_lname, Customer_email in result:
            # Process each row as needed
            customer_object = {
                "customer_id": Customer_ID,
                "first_name": Customer_fname,
                "last_name": Customer_lname,
                "Email": Customer_email
            }
            customers.append(customer_object)  # Append each row to the customers list

        cur.close()

    # if connection to database failed
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB: {}".format(e))

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return customers


# this function selects customer based on their uniquely generate id number
def get_customer_by_id(Customer_id):
    db_connection = None
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """SELECT 
        Customer_ID, Customer_fname, Customer_lname, Customer_email 
        FROM customers WHERE Customer_ID = %s"""
        
        # Execute the query with the provided customer ID
        cur.execute(query, (Customer_id,))
        
        # Fetch the customer record
        result = cur.fetchone()  # Use fetchone() as we expect only one customer
        
        if result:
            # Process the single row
            customer_object = {
                "customer_id": result[0],  # Index 0 contains Customer_ID
                "first_name": result[1],   # Index 1 contains Customer_fname
                "last_name": result[2],    # Index 2 contains Customer_lname
                "Email": result[3]         # Index 3 contains Customer_email
            }
        else:
            # If no customer found with the given ID, return None
            return None
        
        cur.close()

        # Return the customer record
        return customer_object
    
    # if the connection to the database failed
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB: {}".format(e))

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# this function adds a customer record to the database
def add_customer(first_name, last_name, email_address):
    db_connection = None
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database: {db_name}")

        # Using parameterized query to prevent SQL injection
        query = """
            INSERT INTO customers (Customer_fname, Customer_lname, Customer_email)
            VALUES (%s, %s, %s);
            """
        # Execute the query with parameters
        cur.execute(query, (first_name, last_name, email_address))
        
        # Commit changes to the database
        db_connection.commit()
        customer_id = cur.lastrowid
        cur.close()
        new_customer = {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address
        }

        return new_customer

    # if customer has not been commited to database
    except Exception as e:
        raise DbConnectionError("Failed to execute query: {}".format(e))

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# this function selects the holidays from the database by its arrival date
def get_holidays_by_arrival_date(Arrival_date):
    db_connection = None
    holidays_by_date = []
    try:
        db_name = 'HikersHolidays'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """SELECT Holiday_ID, Arrival_date, Duration FROM holidays WHERE Arrival_date = %s"""
        
        # Execute the query with the provided arrival_date
        cur.execute(query, (Arrival_date,))
        
        # Fetch the holiday record
        result = cur.fetchone()  # Fetch a single row
        
        if result:
            # Process the single row
            Holiday_ID, date, duration = result
            formatted_date = date.strftime("%Y-%m-%d")  # Format the date as "YYYY-MM-DD"
            holiday_date_object = {
                "holiday_id": Holiday_ID,
                "arrival_date": formatted_date,
                "duration": duration
            }
            holidays_by_date.append(holiday_date_object)
        else:
            # If no holidays found with the given arrival date
            return None
        
        cur.close()
        return holidays_by_date  # Return the list of holiday objects
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        if db_connection:
            db_connection.close()  # Close the database connection

