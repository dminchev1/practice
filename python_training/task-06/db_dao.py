from psycopg2.extras import RealDictCursor

class EmployeeDbDao:
    def __init__(self, conn):
        self.conn = conn

    def get_all_employees(self, cursor):
        cursor.execute("SELECT * FROM employee")
        employees = cursor.fetchall()
        return employees

    def get_employee_by_id(self, id, cursor):
        cursor.execute("SELECT * FROM employee WHERE id = %s", (id,))
        employee = cursor.fetchone()
        return employee

    def create_employee(self, employee_data, cursor):
        cursor.execute("INSERT INTO employee (first_name, last_name, salary, start_date) VALUES (%s, %s, %s, %s) RETURNING *",
                       (employee_data['first_name'], employee_data['last_name'], employee_data['salary'], employee_data['start_date']))
        new_employee = cursor.fetchone()
        self.conn.commit()
        return new_employee

    def update_employee(self, id, employee_data, cursor):
        cursor.execute("UPDATE employee SET first_name = %s, last_name = %s, salary = %s, start_date = %s WHERE id = %s RETURNING *",
                       (employee_data['first_name'], employee_data['last_name'], employee_data['salary'], employee_data['start_date'], id))
        updated_employee = cursor.fetchone()
        self.conn.commit()
        return updated_employee

    def delete_employee(self, id, cursor):
        cursor.execute("DELETE FROM employee WHERE id = %s", (id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows
