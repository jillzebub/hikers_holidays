from flask import Flask, request, jsonify
from db_utils import (get_holiday_dates, get_customers, add_customer,
                      get_customer_by_id, get_holidays_by_arrival_date, create_reservation)


app = Flask(__name__)


# api endpoint that shows customers
@app.route('/customers', methods=["GET"])
def get_customers_route():
    res = get_customers()
    return jsonify(res)


# api endpoint that shows customer by unique id
@app.route('/customer/<int:Customer_ID>', methods=["GET"])
def get_customers_by_id_route(Customer_ID):
    res = get_customer_by_id(Customer_ID)
    return jsonify(res)


# api endpoint that shows all available holiday dates
@app.route('/holidays/dates', methods=['GET'])
def get_holiday_dates_route():
    res = get_holiday_dates()
    return jsonify(res)


# api endpoint that shows all holidays for a particular date
# http://127.0.0.1:5001/holiday/2024-04-26 - test url
@app.route('/holiday/<string:Arrival_date>', methods=["GET"])
def get_holidays_by_arrival_date_route(Arrival_date):
    res = get_holidays_by_arrival_date(Arrival_date)
    return jsonify(res)


# api endpoint that creates new customer information
@app.route('/customer', methods=['PUT'])
def add_customer_route():
    customer = request.get_json()
    try:
        new_customer = add_customer(
            first_name=customer['first_name'],
            last_name=customer['last_name'],
            email_address=customer['email_address'],
        )
        message = f"Customer {customer['first_name']} added successfully"
        return jsonify({"message": message, "customer": new_customer}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# api endpoint that creates new reservation
@app.route('/reservation', methods=['PUT'])
def put_reservation_route():
    reservation = request.get_json()
    try:
        new_reservation = create_reservation(
            customer_id=reservation['booking_customer_id'],
            holiday_id=reservation['booking_holiday_id'],
        )
        message = f"Reservation successfully added for customer ID {reservation['booking_customer_id']}"
        return jsonify({"message": message, "reservation": new_reservation}), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)

