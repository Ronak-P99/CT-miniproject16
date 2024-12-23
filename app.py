from flask import Flask
from database import db 
from schema import ma
from limiter import limiter
from caching import cache
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from flask_cors import CORS

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.order import Order
from models.product import Product
from models.production import Production
from models.employee import Employee
from models.role import Role
from models.customerManagementRole import CustomerManagementRole
from models.user import User
from models.order_product import order_product

from routes.customerBP import customer_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.customerAccountBP import customer_account_blueprint
from routes.productionBP import production_blueprint
from routes.employeeBP import employee_blueprint
from routes.userAccountBP import user_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "E Commerce API"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://example_sum_postgres_k38e_user:z3ITzoUM4byEsFprhoDgW6ml7AEBExzS@dpg-ctk8hd5umphs73ff80lg-a.oregon-postgres.render.com/example_sum_postgres_k38e'
    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app)

    return app

def blue_print_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    # /customers
    # Because of the blueprint, the '/' would come after '/customers'. Whatever you put in the blueprint would be added after '/customers'
    # '/customers/' 
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(customer_account_blueprint, url_prefix='/accounts')
    app.register_blueprint(production_blueprint, url_prefix='/productions')
    app.register_blueprint(employee_blueprint, url_prefix='/employees')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def configure_rate_limit():
    limiter.limit("5 per day")(customer_blueprint)

def init_customers_info_data():
    with Session(db.engine) as session:
        with session.begin():
            customers = [
                Customer(name="Customer One", email="customer1@example.com",phone="092319283"),
                Customer(name="Customer Two", email="customer2@gmail.com",phone="092319283"),
                Customer(name="Customer Three", email="customer3@hotmail.com",phone="092319283"),
            ]
            customersAccounts = [
                CustomerAccount(username="ctm1", password=generate_password_hash("password1"),customer_id=1),
                CustomerAccount(username="string", password=generate_password_hash("string"),customer_id=2),
                CustomerAccount(username="ctm3", password=generate_password_hash("password3"),customer_id=3),
            ]
            # products = [
            #     Product(name="Product One", price=9.99,quantity_ordered=2, order_id=1),
            #     Product(name="Product Two", price=1.99, quantity_ordered=3, order_id=2),
            #     Product(name="Product Three", price=10.99, quantity_ordered=3, order_id=3),
            # ]
            # orders = [
            #     Order(date="1234-11-12", customer_id=1),
            #     Order(date="1234-11-13", customer_id=2),
            #     Order(date="1234-11-14", customer_id=3),
            # ]
            # employees = [
            #     Employee(name="Employee One", position="Position One"),
            #     Employee(name="Employee Two", position="Position Two"),
            #     Employee(name="Employee Three", position="Position Three"),
            # ]
            # productions = [
            #     Production(name="Production One", quantity_produced=1, product_id=1, employee_id=1, date="1234-11-12"),
            #     Production(name="Production four", quantity_produced=3, product_id=1, employee_id=1, date="1234-11-12"),
            #     Production(name="Production six", quantity_produced=4, product_id=1, employee_id=2, date="1234-11-12"),
            #     Production(name="Production Two", quantity_produced=2, product_id=2, employee_id=2, date="1234-11-13"),
            #     Production(name="Production Three", quantity_produced=8, product_id=3, employee_id=3, date="1234-11-14"),
            # ]
            users = [
                User(username="user1", password=generate_password_hash("pass1")),
                User(username="user2", password=generate_password_hash("pass2")),
                User(username="user3", password=generate_password_hash("pass3"))
            ]
            
            session.add_all(customers)
            session.add_all(customersAccounts)
            # session.add_all(products)
            # session.add_all(orders)
            # session.add_all(employees)
            # session.add_all(productions)
            session.add_all(users)

def init_roles_data():
    with Session(db.engine) as session:
        with session.begin():
            roles = [
                Role(role_name='admin'),
                Role(role_name='user'),
                Role(role_name='guest'),
            ]
            session.add_all(roles)

def init_roles_customers_data():
    with Session(db.engine) as session:
        with session.begin():
            roles_customers = [
                CustomerManagementRole(customer_management_id=1, user_management_id=1, role_id=1),
                CustomerManagementRole(customer_management_id=2, user_management_id=2, role_id=2),
                CustomerManagementRole(customer_management_id=3, user_management_id=3, role_id=3)
            ]
            session.add_all(roles_customers)



    app = create_app('DevelopmentConfig')

    blue_print_config(app)
    configure_rate_limit()

    with app.app_context():
        db.drop_all()
        db.create_all()
        init_roles_data()
        init_customers_info_data()
        init_roles_customers_data()

    app.run(debug=True)