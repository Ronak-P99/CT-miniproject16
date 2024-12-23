import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from models.employee import Employee
from models.product import Product
from models.production import Production
from models.customer import Customer
from models.order import Order
from app import create_app
from datetime import datetime
from database import db
from services.productionService import save



class TestProductions(unittest.TestCase):   
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.production = Production(name="Production One", quantity_produced=1, product_id=1, employee_id=1, date=datetime.strptime("1234-11-12", "%Y-%m-%d"))
        self.product = Product(name="Product One", price=9.99, quantity_ordered=1, order_id=1)
        self.order = Order(date=datetime.strptime("1900-01-01", "%Y-%m-%d").date(), customer_id=1)
        self.employee = Employee(name="Employee One", position="Position One")
        self.customer = Customer(name="Customer One", email="customer1@gmail.com",phone="092319283")

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.product)
            db.session.add(self.order)
            db.session.add(self.employee)
            db.session.add(self.customer)
            db.session.add(self.production)

            db.session.commit()
        self.client = self.app.test_client()


    def test_create_production(self):
        production_payload = {"name": "Production One", "quantity_produced": 1, "product_id": 1, "employee_id": 1, "date": "1234-11-12"}
        response = self.client.post("/productions/", json = production_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Production One")

    def test_get_productions(self):
        response = self.client.get("/productions/")
        print(response.json)

    def test_get_production_dates(self):
        response2 = self.client.get("/productions/quantity-dates")
        print(response2.json)
    
    @patch('services.productionService.db.session.execute') # replacing the db.session.execute with a mock object for testing
    def test_production_save(self, mock_employee):
            # Set up the return value for the mock object
            faker = Faker()
            production_data = {"name": faker.name(), "quantity_produced": faker.random_digit(),  "employee_id": 1,  "date": "1900-01-01", "product_id": 1 } # simulate a user retrieved from the database

            # mock_customer.return_value.scalar_one_or_none.return_value = mock_user

            response = save(production_data)

            self.assertEqual(response.name, production_data["name"])



if __name__ == '__main__':
    unittest.main()