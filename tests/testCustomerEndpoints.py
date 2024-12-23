import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from services.customerService import save
from models.customer import Customer
from models.product import Product
from models.order import Order
from app import create_app, init_customers_info_data
from datetime import datetime
from database import db



class TestCustomer(unittest.TestCase):   
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.customer = Customer(name="Customer One", email="customer1@gmail.com",phone="092319283")
        self.order = Order(date=datetime.strptime("1900-01-01", "%Y-%m-%d").date(), customer_id=1)
        self.product = Product(name="Product One", price=9.99,quantity_ordered=1, order_id=1)
        with self.app_context:
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.order)
            db.session.add(self.product)
            db.session.commit()
        self.client = self.app.test_client()


    def test_create_customer(self):
        customer_payload = {"name": "Customer One", "email": "customer1@gmail.com", "phone": "1234567890"}
        response = self.client.post("/customers/", json = customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Customer One")

    def test_find_gmail(self):
        response2 = self.client.get("/customers/gmail")
        print(response2.json)
        self.assertEqual(response2.json[0]["name"], "Customer One" )

    def test_get_customers_orders(self):
        response2 = self.client.get("/customers/price-total")
        print(response2.json)

    @patch('services.customerService.db.session.execute') # replacing the db.session.execute with a mock object for testing
    def test_customer_save(self, mock_customer):
        # Set up the return value for the mock object
        faker = Faker()
        customer_data = {"name": faker.name(), "email": faker.ascii_email(), "phone": faker.phone_number()} # simulate a user retrieved from the database

        # mock_customer.return_value.scalar_one_or_none.return_value = mock_user

        response = save(customer_data)

        self.assertEqual(response.name, customer_data["name"])

    

if __name__ == '__main__':
    unittest.main()