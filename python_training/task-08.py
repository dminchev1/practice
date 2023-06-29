# Unit test of dbdao layer methods
import unittest
from unittest.mock import MagicMock
import os, sys
sys.path.append(os.getcwd() + '/task-06')
from db_dao import EmployeeDbDao


class TestEmployeeDbDao(unittest.TestCase):
    """Automated testing locally with Python's unittest.
    """
    
    def setUp(self):
        # Mock the database connection and cursor
        self.conn = MagicMock()
        self.cursor = self.conn.cursor.return_value

        # Create an instance of EmployeeDbDao with the mocked connection
        self.dao = EmployeeDbDao(self.conn)

    def test_get_all_employees(self):
        # Mock the fetchall method to return sample employee data
        # Ideally more records to test on
        self.cursor.fetchall.return_value = [
            {'first_name': 'Mike', 'id': 3, 'last_name': 'Johnson', 'salary': 7000.0, 'start_date': 'Wed, 01 Mar 2023 00:00:00 GMT'},
            {'first_name': 'John', 'id': 4, 'last_name': 'Doe', 'salary': 5000.0, 'start_date': 'Sun, 01 Jan 2023 00:00:00 GMT'}
        ]

        # Call the method under test, passing the mocked cursor
        employees = self.dao.get_all_employees(self.cursor)

        # Assertions
        self.cursor.execute.assert_called_once_with("SELECT * FROM employee")
        self.assertEqual(employees, self.cursor.fetchall.return_value)
    
    def test_get_employee_by_id(self):
        # Mock the fetchone method to return a sample employee
        self.cursor.fetchone.return_value = {'first_name': 'Mike', 'id': 3, 'last_name': 'Johnson', 'salary': 7000.0, 'start_date': 'Wed, 01 Mar 2023 00:00:00 GMT'}

        # Call the method under test, passing the mocked cursor
        employee = self.dao.get_employee_by_id(3, self.cursor)

        # Assertions
        self.cursor.execute.assert_called_once_with("SELECT * FROM employee WHERE id = %s", (3,))
        self.assertEqual(employee, self.cursor.fetchone.return_value)

    def test_create_employee(self):
        # Mock the execute and fetchone methods to simulate creating a new employee
        self.cursor.fetchone.return_value = {'first_name': 'John', 'id': 5, 'last_name': 'Smith', 'salary': 6000.0, 'start_date': 'Tue, 01 Feb 2023 00:00:00 GMT'}

        # Create a sample employee data
        employee_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'salary': 6000.0,
            'start_date': '2023-02-01'
        }

        # Call the method under test, passing the mocked cursor and sample employee data
        new_employee = self.dao.create_employee(employee_data, self.cursor)

        # Assertions
        self.cursor.execute.assert_called_once_with("INSERT INTO employee (first_name, last_name, salary, start_date) VALUES (%s, %s, %s, %s) RETURNING *",
                                                    (employee_data['first_name'], employee_data['last_name'], employee_data['salary'], employee_data['start_date']))
        self.conn.commit.assert_called_once()  # Check if commit was called
        self.assertEqual(new_employee, self.cursor.fetchone.return_value)

    def test_update_employee(self):
        # Mock the execute and fetchone methods to simulate updating an employee
        self.cursor.fetchone.return_value = {'first_name': 'John', 'id': 5, 'last_name': 'Smith', 'salary': 7000.0, 'start_date': 'Tue, 01 Feb 2023 00:00:00 GMT'}

        # Update employee data
        employee_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'salary': 7000.0,
            'start_date': '2023-02-01'
        }

        # Call the method under test, passing the employee ID, updated data, and mocked cursor
        updated_employee = self.dao.update_employee(5, employee_data, self.cursor)

        # Assertions
        self.cursor.execute.assert_called_once_with("UPDATE employee SET first_name = %s, last_name = %s, salary = %s, start_date = %s WHERE id = %s RETURNING *",
                                                    (employee_data['first_name'], employee_data['last_name'], employee_data['salary'], employee_data['start_date'], 5))
        self.conn.commit.assert_called_once()  # Check if commit was called
        self.assertEqual(updated_employee, self.cursor.fetchone.return_value)

    def test_delete_employee(self):
        # Mock the rowcount attribute to simulate deleting an employee
        self.cursor.rowcount = 1

        # Delete employee by ID
        deleted_rows = self.dao.delete_employee(20, self.cursor)

        # Assertions
        self.cursor.execute.assert_called_once_with("DELETE FROM employee WHERE id = %s", (20,))
        self.conn.commit.assert_called_once()  # Check if commit was called
        self.assertEqual(deleted_rows, self.cursor.rowcount)



if __name__ == '__main__':
    unittest.main()

        

