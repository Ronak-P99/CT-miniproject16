from sqlalchemy import select, func
from models.customer import Customer
from models.customerAccount import CustomerAccount
from database import db
from utils.util import encode_token
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from circuitbreaker import circuit
from werkzeug.security import generate_password_hash



def fallback_function(customeraccount):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_account_data):
    with Session(db.engine) as session:
        with session.begin():
            customer_id = customer_account_data['customer_id']
            customer = session.execute(select(Customer).where(Customer.id == customer_id)).scalars().first()
           
            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")
            
            new_customer_account = CustomerAccount(username=customer_account_data['username'], password=generate_password_hash(customer_account_data['password']), customer_id=customer_account_data['customer_id'])
            session.add(new_customer_account)
            print("New Customer Account ID (before commit):", new_customer_account.id)
            session.flush()
            print("New Customer Account ID (after commit):", new_customer_account.id)
            session.commit() 

        session.refresh(new_customer_account)
        return new_customer_account

def find_by_id(id):
    query = select(CustomerAccount).join(Customer).where(Customer.id == CustomerAccount.customer_id).filter_by(id=id)
    customeraccount = db.session.execute(query).scalar_one_or_none()
    return customeraccount

def update(id, customer_account_data):
    customer = find_by_id(id)
           
    if not customer:
        raise ValueError(f"Customer with ID {id} does not exist")

    customer.username = customer_account_data['username']
    customer.password = generate_password_hash(customer_account_data['password'])
    
    
    db.session.commit()

    return customer

def delete(id):
    customer = find_by_id(id)
           
    if not customer:
        raise ValueError(f"Customer with ID {id} does not exist")
    
    db.session.delete(customer)
    db.session.commit()

    return "Successfully deleted"
    

def find_all():
    query = select(CustomerAccount)
    customer_accounts = db.session.execute(query).scalars().all()
    return customer_accounts

def login_customer(username, password):
    user = (db.session.execute(db.select(CustomerAccount).where(CustomerAccount.username == username)).scalar_one_or_none())
    role_names = [role.role_name for role in user.roles]
    if user:
        if check_password_hash(user.password, password):    
            auth_token = encode_token(user.id, role_names)
            resp = {
                "status": "success",
                "message": "Successfully logged in",
                "auth_token": auth_token
            }
            return resp
        else:
            return None
