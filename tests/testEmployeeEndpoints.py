import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from services.employeeService import save
from models.employee import Employee
from models.product import Product
from models.production import Production
from models.customer import Customer
from models.order import Order
from app import create_app
from datetime import datetime
from database import db



class TestEmployee(unittest.TestCase):   
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.employee = Employee(name="Employee One", position="Position One")
        self.customer = Customer(name="Customer One", email="customer1@gmail.com",phone="092319283")
        self.order = Order(date=datetime.strptime("1900-01-01", "%Y-%m-%d").date(), customer_id=1)
        self.product = Product(name="Product One", price=9.99,quantity_ordered=1, order_id=1)
        self.production = Production(name="Production One", quantity_produced=1, product_id=1, employee_id=1, date=datetime.strptime("1234-11-12", "%Y-%m-%d"))

        with self.app_context:
            db.drop_all()
            db.create_all()
            db.session.add(self.employee)
            db.session.add(self.customer)
            db.session.add(self.order)
            db.session.add(self.product)
            db.session.add(self.production)

            db.session.commit()
        self.client = self.app.test_client()


    def test_create_employee(self):
        employee_payload = {"name": "Employee One", "position": "Position One"}
        response = self.client.post("/employees/", json = employee_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Employee One")

    def test_get_employee(self):
        response2 = self.client.get("/employees/")
        print(response2.json)

    def test_employee_production(self):
        response2 = self.client.get("/employees/production-report")
        print(response2.json)

    @patch('services.employeeService.db.session.execute') # replacing the db.session.execute with a mock object for testing
    def test_employee_save(self, mock_employee):
        # Set up the return value for the mock object
        faker = Faker()
        employee_data = {"name": faker.name(), "position": faker.job()} # simulate a user retrieved from the database

        # mock_customer.return_value.scalar_one_or_none.return_value = mock_user

        response = save(employee_data)

        self.assertEqual(response.name, employee_data["name"])



if __name__ == '__main__':
    unittest.main()