import requests


# display dates function
def display_dates(records):  # Show the customer all available holiday dates, durations
    print("{:<30} {:<20} {:<15}".format(
        'Arrival Date', 'Number of nights', 'Holiday ID'
    ))
    print('-' * 62)

    for item in records:
        date_str = item['arrival_date'][:16]  # Truncate the date string if needed
        print("{:<30} {:<20} {:<15}".format(
            date_str, item['duration'], item['holiday_id']
        ))


# shows the user all the available holiday dates
def get_holidays():
    result = requests.get(
        'http://127.0.0.1:5001/holidays/dates',
        headers={'content-type': 'application/json'}
    )
    return result.json()


# if customer id is yes then customer is found in the database
def find_customer(customer_id_entered):
    response = requests.get(
       f'http://127.0.0.1:5001/customer/{customer_id_entered}',
       headers={'content-type': 'application/json'}
    )
    data = response.json()
    if 'error' in data:
        print("Error:", data['error'])
        return None
    else:
        customer = {'first_name': data['first_name'], 'customer_id': data['customer_id']}
        return customer


# if customer is no then customer id is added to the database
def enter_new_customer(new_customer_data):
    response = requests.put(
        'http://127.0.0.1:5001/customer',
        json=new_customer_data,
        headers={'content-type': 'application/json'}
    )

    if response.status_code == 201:
        data = response.json()
        customer = data["customer"]
        print("New customer created successfully!", customer)
    else:
        print("Failed to create a new customer.")


# find holiday in the database that matches inputted date by user
def find_holidays_by_date(entered_arrival_date):
    response = requests.get(
       f'http://127.0.0.1:5001/holiday/{entered_arrival_date}',
       headers={'content-type': 'application/json'}
    )
    data = response.json()
    if 'error' in data:
        print("Error:", data['error'])
        return None
    else:
        return data


# adds reservation to the database for holiday id and customer id
def enter_new_reservation(new_reservation_data):
    response = requests.put(
        'http://127.0.0.1:5001/reservation',
        json=new_reservation_data,
        headers={'content-type': 'application/json'}
    )

    if response.status_code == 201:
        data = response.json()
        reservation = data["reservation"]
        print(reservation)
    else:
        print("Failed to create booking.")


# run function that runs front end and asks user for input which will be used as the arguments for functions above
def run():
    print("Welcome to Hikers' Holidays, the friendliest glamping site in Aviemore!")

    print()
    holiday_dates = get_holidays()  # Fetch holiday dates
    if not holiday_dates:
        print('There are no holidays available.')
        return
    
    print("The available holidays are: ")
    print()
    display_dates(holiday_dates)  # Display holiday dates
    print()

    # Check if customer has id
    customer_has_id = input("Do you have a customer login? (yes/no): ").lower()
    
    # if customer has id greet them
    if customer_has_id == "yes":
        customer_id_entered = input("Please enter your customer ID: ")
        customer = find_customer(customer_id_entered)
        if customer:
            print(f"Hi {customer['first_name']}!")
        else:
            print("Customer not found.")  # error message if customer not found

    # if customer doesn't have an id create one and enter data into database
    else:
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        email_address = input("Please enter your email: ")
        new_customer_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address
        }
        try:
            enter_new_customer(new_customer_data)
            print("You've been successfully registered as a new customer!")
        except Exception as e:
            print("Failed to register customer:", e)  # error message if failed to create a new customer

    # enter chosen arrival date, search database for matching holidays and display
    entered_arrival_date = input("Please enter your desired arrival date (YYYY-MM-DD): ")
   
    print()
    holidays_by_date = find_holidays_by_date(entered_arrival_date)
    if not holidays_by_date:
        print('There are no holidays available for this date')

    print(f"The available holidays for {entered_arrival_date} are:")
    print()
    display_dates(holidays_by_date)  # display holidays for date
    print()

    # create reservation using inputted customer id and holiday id as generated and viewed above
    booking_customer_id = input("Enter customer ID to confirm booking: ")

    booking_holiday_id = input("Enter the holiday ID you wish to book: ")
    new_reservation_data = {
        'booking_customer_id': booking_customer_id,
        'booking_holiday_id': booking_holiday_id
    }
    try:
        enter_new_reservation(new_reservation_data)
        print(f"Reservation for holiday {booking_holiday_id} successfully created!")
    except Exception as e:
        print("Failed to book holiday:", e)

   
if __name__ == "__main__":
    run()

