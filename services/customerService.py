from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from circuitbreaker import circuit
from sqlalchemy import select, func
from models.product import Product
from models.order import Order

def fallback_function(customer):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data['name'] == "Failure":
            raise Exception("Failure condition triggered")
        
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                session.add(new_customer)
                savepoint = session.begin_nested()

                try:
                    # Do query / transaction here
                    # Start a nested transaction and stablish a savepoint
                    new_nested_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                    session.add(new_nested_customer)
                except:
                    # Rollback the nested transaction to the savepoint
                    savepoint.rollback()

            session.refresh(new_customer)
            return new_customer
        
    except Exception as e:
           raise e
    
def find_by_id(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalar_one_or_none()
    return customer

def update(id, customer_data):
    customer = find_by_id(id)
           
    if not customer:
        raise ValueError(f"Customer with ID {id} does not exist")

    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']    
    
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
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers

def find_customers_gmail():
    query = select(Customer).where(Customer.email.like("%gmail%"))
    customers = db.session.execute(query).scalars().all()

    return customers

def find_all_pagination(page=1, per_page=10):
    customers = db.paginate(select(Customer), page=page, per_page=per_page)
    return customers


def get_customers_orders():
    results = db.session.query(
        Customer.name,
        func.sum(Product.price).label('total_price_ordered')
    ).join(Order, Customer.id == Order.customer_id).join(Product, Order.id == Product.order_id) \
    .group_by(Customer.name) \
    .having(func.sum(Product.price) > 5) \
    .order_by(func.sum(Product.price).desc()) \
    .all()

    return [{'customer_name': name, 'total_price_ordered': total} for name, total in results]

