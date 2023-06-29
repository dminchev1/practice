class EmployeeService:
    '''Business layer that allows scalability and 
    custom functions request from the business side.
    '''
    def __init__(self, employee_dao):
        self.employee_dao = employee_dao

    def get_all_employees(self):
        return self.employee_dao.get_all_employees()

    def get_employee_by_id(self, id):
        return self.employee_dao.get_employee_by_id(id)

    def create_employee(self, employee_data):
        return self.employee_dao.create_employee(employee_data)

    def update_employee(self, id, employee_data):
        return self.employee_dao.update_employee(id, employee_data)

    def delete_employee(self, id):
        return self.employee_dao.delete_employee(id)