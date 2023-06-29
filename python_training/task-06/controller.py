import psycopg2
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from service import EmployeeService
from db_dao import EmployeeDbDao

app = Flask(__name__)

# GET request to /employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = employee_service.get_all_employees()
    return jsonify(employees)

# GET request to /employees/{id}
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = employee_service.get_employee_by_id(id)
    if employee:
        return jsonify(employee)
    else:
        return jsonify({'error': 'Employee not found'}), 404

# POST request to /employees
@app.route('/employees', methods=['POST'])
def create_employee():
    employee_data = request.get_json()
    new_employee = employee_service.create_employee(employee_data)
    if new_employee:
        return jsonify(new_employee), 201
    else:
        return jsonify({'message': 'Error'}), 500

# PUT request to /employees/{id}
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee_data = request.get_json()
    updated_employee = employee_service.update_employee(id, employee_data)
    if updated_employee:
        return jsonify(updated_employee)
    else:
        return jsonify({'error': 'Employee not found'}), 404

# DELETE request to /employees/{id}
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    deleted_rows = employee_service.delete_employee(id)
    if deleted_rows > 0:
        return jsonify({'message': 'Employee deleted'})
    else:
        return jsonify({'error': 'Employee not found'}), 404

# HEAD request to /employees/{id}
@app.route('/employees/<int:id>', methods=['HEAD'])
def check_employee(id):
    employee = employee_service.get_employee_by_id(id)
    if employee:
        return jsonify({'message': '200'})
    else:
        return jsonify({'message': '404'})

# Swagger specific - In progress
# Following https://sean-bradley.medium.com/add-swagger-ui-to-your-python-flask-api-683bfbb32b36
# https://code.likeagirl.io/swagger-and-postman-build-a-swagger-ui-for-your-python-flask-application-141bb4d0c203
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi_employees.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': "Emplyee API"
  }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    # Connection parameters
    dbname = 'postgres'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'

    # Create connection
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=dbname,
        user=user,
        password=password
    )

    # Initialize Employee Service with Employee DB DAO
    employee_dao = EmployeeDbDao(conn)
    employee_service = EmployeeService(employee_dao)

    app.run(debug=True)