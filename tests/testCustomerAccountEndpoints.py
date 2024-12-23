import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from werkzeug.security import generate_password_hash
from services.customerAccountService import login_customer


class TestLoginCustomer(unittest.TestCase):


    @patch('services.customerAccountService.db.session.execute') # replacing the db.session.execute with a mock object for testing
    def test_login_customer(self, mock_customer):
        # Set up the return value for the mock object
        faker = Faker()
        mock_user = MagicMock() # simulate a user retrieved from the database
        mock_user.id = 1
        mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_user.username = faker.user_name() # Generate a random username
        mock_user.password = generate_password_hash(password) # Generate a random password and hash it
        mock_customer.return_value.scalar_one_or_none.return_value = mock_user

        response = login_customer(mock_user.username, password)

        self.assertEqual(response['status'], 'success')

    @patch('services.customerAccountService.db.session.execute') # replacing the db.session.execute with a mock object for testing
    def test_fail_login(self, mock_customer):
        # Set up the return value for the mock object
        faker = Faker()
        mock_user = MagicMock() # simulate a user retrieved from the database
        mock_user.id = 1
        mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_user.username = faker.user_name() # Generate a random username
        mock_user.password = generate_password_hash(password) # Generate a random password and hash it
        mock_customer.query.filter.return_value.one_or_none.return_value = mock_user

        # Call the login_customer function with the test data
        response = login_customer(mock_user.username, faker.password()) # call with other generate password
        #                                           passwordA != passwordB -> return None

        # Check the response status
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()