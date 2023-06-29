from abc import ABC, abstractmethod

class EmployeeDao(ABC):
    @abstractmethod
    def get_all_employees(self):
        raise NotImplemented

    @abstractmethod
    def get_employee_by_id(self, id):
        raise NotImplemented

    @abstractmethod
    def create_employee(self, employee_data):
        raise NotImplemented

    @abstractmethod
    def update_employee(self, id, employee_data):
        raise NotImplemented

    @abstractmethod
    def delete_employee(self, id):
        raise NotImplemented